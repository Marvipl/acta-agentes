#!/usr/bin/env python3
"""bot.py — Assistente Estratégico da Acta Robotics em TEMPO REAL.

Servidor Slack (Socket Mode — sem URL pública) que, a cada mensagem no canal
de estratégia (ou @menção em outro canal), roda uma sessão do Claude Agent SDK
com o playbook assistente-estrategico/SKILL.md e responde na thread.

Variáveis de ambiente obrigatórias:
  SLACK_BOT_TOKEN          token do bot (xoxb-...)
  SLACK_APP_TOKEN          token de app-level p/ Socket Mode (xapp-..., scope connections:write)
  SLACK_CHANNEL_ID         ID do canal de estratégia (#estrategia)
  SLACK_STAFF_CHANNEL_ID   ID do canal do staff (dash e resumos)
  ANTHROPIC_API_KEY        chave da API da Anthropic (cobrança por token)

Opcionais:
  GOOGLE_SERVICE_ACCOUNT_FILE  JSON da service account com leitura na pasta Acta/ do Drive
  DRIVE_DOC_PLANEJAMENTO       nome exato do doc de planejamento estratégico
  BOT_MAX_TURNS                limite de turnos do agente por resposta (padrão 40)

Rodar: python3 assistente-estrategico/bot/bot.py  (a partir da raiz do repo ou de onde for)
"""
import asyncio
import json
import logging
import os
import threading
from pathlib import Path

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from claude_agent_sdk import ClaudeAgentOptions, query

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("assistente-estrategico")

BOT_DIR = Path(__file__).resolve().parent
RAIZ = BOT_DIR.parents[1]  # raiz do repo acta-agentes
SESSOES_PATH = BOT_DIR / ".sessoes.json"  # thread_ts -> session_id (continuidade por thread)

CANAL_ESTRATEGIA = os.environ["SLACK_CHANNEL_ID"]
MAX_TURNS = int(os.environ.get("BOT_MAX_TURNS", "40"))
LIMITE_MSG = 3800  # divisão de respostas longas em várias mensagens do Slack

app = App(token=os.environ["SLACK_BOT_TOKEN"])

_lock = threading.Lock()
_tratados: set[str] = set()  # ts de eventos já processados (dedup de retries do Slack)


def _prompt_sistema() -> str:
    modo = (BOT_DIR / "prompt_bot.md").read_text(encoding="utf-8")
    skill = (RAIZ / "assistente-estrategico" / "SKILL.md").read_text(encoding="utf-8")
    return modo + "\n\n---\n\nPLAYBOOK (assistente-estrategico/SKILL.md):\n\n" + skill


def _sessoes() -> dict:
    try:
        return json.loads(SESSOES_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _salvar_sessao(thread_ts: str, session_id: str) -> None:
    with _lock:
        dados = _sessoes()
        dados[thread_ts] = session_id
        # mantém só as 200 threads mais recentes
        if len(dados) > 200:
            for k in sorted(dados)[: len(dados) - 200]:
                del dados[k]
        SESSOES_PATH.write_text(json.dumps(dados, indent=2), encoding="utf-8")


async def _rodar_agente(prompt: str, resume: str | None) -> tuple[str | None, str | None]:
    opts = ClaudeAgentOptions(
        cwd=str(RAIZ),
        system_prompt=_prompt_sistema(),
        allowed_tools=["Bash", "Read", "Grep", "Glob", "WebSearch", "WebFetch"],
        permission_mode="bypassPermissions",
        max_turns=MAX_TURNS,
        resume=resume,
    )
    texto: str | None = None
    session_id: str | None = resume
    async for m in query(prompt=prompt, options=opts):
        nome = type(m).__name__
        if nome == "AssistantMessage":
            partes = [getattr(b, "text", None) for b in getattr(m, "content", [])]
            partes = [p for p in partes if p]
            if partes:
                texto = "\n".join(partes)
        elif nome == "ResultMessage":
            session_id = getattr(m, "session_id", None) or session_id
            texto = getattr(m, "result", None) or texto
    return texto, session_id


def _dividir(texto: str) -> list[str]:
    partes, atual = [], ""
    for linha in texto.split("\n"):
        if len(atual) + len(linha) + 1 > LIMITE_MSG:
            partes.append(atual)
            atual = linha
        else:
            atual = f"{atual}\n{linha}" if atual else linha
    if atual:
        partes.append(atual)
    return partes or [texto[:LIMITE_MSG]]


def _tratar(event: dict, client) -> None:
    ts = event["ts"]
    with _lock:
        if ts in _tratados:
            return
        _tratados.add(ts)
        if len(_tratados) > 1000:
            _tratados.clear()
            _tratados.add(ts)

    canal = event["channel"]
    thread_ts = event.get("thread_ts") or ts
    autor = event.get("user", "")
    texto_usuario = event.get("text", "").strip()
    if not texto_usuario and not event.get("files"):
        return

    try:  # sinaliza que a mensagem foi vista (requer scope reactions:write)
        client.reactions_add(channel=canal, name="eyes", timestamp=ts)
    except Exception:
        pass

    anexos = [
        {"name": f.get("name"), "mimetype": f.get("mimetype"), "url_private": f.get("url_private")}
        for f in event.get("files", [])
    ]
    bloco_anexos = (
        "\n\nAnexos da mensagem (baixe com estrategia.sh baixar <url_private> <destino>):\n"
        + json.dumps(anexos, ensure_ascii=False)
        if anexos
        else ""
    )
    resume = _sessoes().get(thread_ts)
    prompt = (
        f"Mensagem recebida AGORA no Slack — canal {canal}, thread {thread_ts}, "
        f"autor <@{autor}>:\n\n{texto_usuario}{bloco_anexos}\n\n"
        "Responda seguindo o método do playbook. O texto final da sua resposta será "
        "postado na thread pelo servidor — NÃO use scripts para postar mensagens "
        "(exceção: envio de ARQUIVO gerado, via estrategia.sh arquivo)."
    )
    log.info("processando %s (thread %s, resume=%s)", ts, thread_ts, bool(resume))
    try:
        resposta, session_id = asyncio.run(_rodar_agente(prompt, resume))
    except Exception as exc:  # resposta nunca fica em silêncio por erro interno
        log.exception("erro no agente")
        resposta, session_id = (
            f"⚠️ Não consegui processar agora ({type(exc).__name__}). Tente de novo em instantes.",
            resume,
        )
    if session_id:
        _salvar_sessao(thread_ts, session_id)

    for parte in _dividir(resposta or "⚠️ Não consegui gerar uma resposta — tente reformular."):
        client.chat_postMessage(channel=canal, text=parte, thread_ts=thread_ts)
    log.info("respondido %s", ts)


@app.event("message")
def on_message(event, client):
    # no canal de estratégia, TODA mensagem humana nova (inclusive replies em
    # thread) é tratada; noutros canais este handler ignora (lá vale a @menção)
    if event.get("channel") != CANAL_ESTRATEGIA:
        return
    if event.get("subtype") or event.get("bot_id"):
        return
    _tratar(event, client)


@app.event("app_mention")
def on_mention(event, client):
    # @menção fora do canal de estratégia (no canal, o handler de message cobre)
    if event.get("channel") == CANAL_ESTRATEGIA:
        return
    if event.get("bot_id"):
        return
    _tratar(event, client)


if __name__ == "__main__":
    faltando = [v for v in ("SLACK_APP_TOKEN", "SLACK_STAFF_CHANNEL_ID", "ANTHROPIC_API_KEY") if not os.environ.get(v)]
    if faltando:
        raise SystemExit(f"Variáveis de ambiente faltando: {', '.join(faltando)}")
    log.info("Assistente Estratégico em tempo real — canal %s, repo %s", CANAL_ESTRATEGIA, RAIZ)
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
