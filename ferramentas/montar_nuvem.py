"""Monta a configuração da raiz do repositório para rodar todos os squads numa sessão de nuvem do Claude Code.

Na nuvem a sessão começa na raiz do repositório, e só o .claude/ da raiz carrega agentes e configurações.
Este script lê cada pasta squad-*/ e gera na raiz:
  .claude/agents/<prefixo>-<agente>.md   agentes de cada squad com prefixo (evita nomes repetidos entre squads)
  .claude/commands/<comando>.md          comandos de cada squad (repetidos ganham o nome do squad: anexar-orcamento)
  .claude/settings.json                  regras de bloqueio dos squads + hook de preparação da nuvem (mescla com o que já existe)
  CLAUDE.md                              bloco entre <!-- squads:inicio --> e <!-- squads:fim --> (o resto do arquivo é preservado)
  .gitignore                             bloco de segurança (dados, chaves, bancos locais)
Só regrava arquivos que ele mesmo gerou (lista em .claude/.squads_gerado.json). Rode de novo sempre que um squad mudar.

Uso (na raiz do repositório):  python ferramentas/montar_nuvem.py [--simular]
"""
import argparse, json, re, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
MANIFESTO = RAIZ / ".claude" / ".squads_gerado.json"
PREFIXOS = {"squad-orcamento": "orc", "squad-estrategia": "est", "squad-produto": "prod", "squad-analise": "dados"}
NOMES = {"squad-orcamento": "orçamento", "squad-estrategia": "estratégia", "squad-produto": "produto", "squad-analise": "análise de dados"}
FM = re.compile(r"^---\n(.*?)\n---\n", re.S)


def _fm(txt):
    m = FM.match(txt)
    if not m:
        return {}, txt
    campos = {}
    for linha in m.group(1).splitlines():
        if ":" in linha:
            k, v = linha.split(":", 1); campos[k.strip()] = v.strip()
    return campos, txt[m.end():]


def _desc(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] == '"':
        v = v[1:-1].replace('\\"', '"')
    return v


def _primeira_frase(t, limite=220):
    t = re.split(r"(?<=[.!?])\s", t.strip(), maxsplit=1)[0]
    return t if len(t) <= limite else t[:limite - 1].rstrip() + "…"


def _cabecalho(squad, prefixo):
    return (f"> **Squad de {NOMES.get(squad, squad)}** · pasta `{squad}/`. Rode os comandos do motor a partir dessa pasta "
            f"(`cd {squad} && python -m motor...`); caminhos relativos como `nos/`, `projetos/` e `conhecimento/` são relativos a ela. "
            f"Leia `{squad}/CLAUDE.md`. Neste repositório os agentes deste squad têm o prefixo `{prefixo}-`: quando o texto citar o agente "
            f"`nome`, o agente registrado é `{prefixo}-nome`.\n\n")


def montar(simular=False):
    squads = sorted(p for p in RAIZ.glob("squad-*") if (p / ".claude").is_dir())
    if not squads:
        sys.exit("Nenhuma pasta squad-*/ com .claude/ encontrada na raiz.")
    antes = set(json.loads(MANIFESTO.read_text(encoding="utf-8"))["arquivos"]) if MANIFESTO.exists() else set()
    gerar, conflitos = {}, []
    cmds_por_nome = {}
    for s in squads:
        for c in (s / ".claude" / "commands").glob("*.md"):
            cmds_por_nome.setdefault(c.stem, []).append(s.name)
    destinos = json.loads((RAIZ / "ferramentas" / "squads.json").read_text(encoding="utf-8")) if (RAIZ / "ferramentas" / "squads.json").exists() else {}
    deny, resumo = set(), []
    for s in squads:
        pre = PREFIXOS.get(s.name, s.name.replace("squad-", "")); cab = _cabecalho(s.name, pre); n_ag = 0
        for a in sorted((s / ".claude" / "agents").glob("*.md")):
            campos, corpo = _fm(a.read_text(encoding="utf-8"))
            nome = f"{pre}-{campos.get('name', a.stem)}"
            desc = f"[Squad de {NOMES.get(s.name, s.name)}] " + _primeira_frase(_desc(campos.get("description", "")))
            fm = f"---\nname: {nome}\ndescription: \"{desc.replace(chr(34), chr(39))}\"\n"
            for k in ("tools", "model"):
                if k in campos: fm += f"{k}: {campos[k]}\n"
            gerar[f".claude/agents/{nome}.md"] = fm + "---\n\n" + cab + corpo
            n_ag += 1
        cmds = []
        for c in sorted((s / ".claude" / "commands").glob("*.md")):
            campos, corpo = _fm(c.read_text(encoding="utf-8"))
            nome = c.stem if len(cmds_por_nome[c.stem]) == 1 else f"{c.stem}-{s.name.replace('squad-', '')}"
            corpo = corpo.replace("`.claude/skills/", f"`{s.name}/.claude/skills/")
            fm = "---\n" + "".join(f"{k}: {v}\n" for k, v in campos.items() if k != "description")
            d_cmd = f"[Squad de {NOMES.get(s.name, s.name)}] {_desc(campos.get('description', ''))}".replace('"', "'")
            fm = fm.replace("---\n", f"---\ndescription: \"{d_cmd}\"\n", 1)
            if c.stem in (destinos.get(s.name) or {}).get("publicar_ao_final", []):
                corpo = corpo.rstrip() + (
                    f"\n\n**Publicação automática: passo final obrigatório, sem esperar novo pedido.** Assim que a versão for congelada "
                    f"(ou, se o fluxo não congelar, assim que Marcus aprovar o último portão), publique:\n"
                    f"- na nuvem (variável de ambiente `CLAUDE_CODE_REMOTE=true`): siga `.claude/commands/publicar-drive.md` com `{s.name}` e a pasta da versão, "
                    f"enviando o pacote completo (documentos finais e metadados) para `{(destinos.get(s.name) or {}).get('drive', 'Acta')}`. Se não houver `ACTA_DRIVE_CREDENCIAL` nem conector do Google Drive "
                    f"habilitado na sessão, peça a Marcus para habilitar e publique logo em seguida;\n"
                    f"- no computador: `cd {s.name} && python -m motor.publicar <pasta da versão>`.\n"
                    f"Termine a resposta final com o link da pasta no Drive e o total de arquivos publicados.\n")
            gerar[f".claude/commands/{nome}.md"] = fm + "---\n" + cab + corpo
            cmds.append("/" + nome)
        st = s / ".claude" / "settings.json"
        if st.exists():
            deny |= set((json.loads(st.read_text(encoding="utf-8")).get("permissions") or {}).get("deny") or [])
        resumo.append((s.name, pre, n_ag, cmds))
    gerar[".claude/commands/publicar-drive.md"] = (
        '---\ndescription: "Publica no Google Drive o pacote completo de uma versão: documentos finais e metadados (JSON, CSV, planilha, nós, revisões), igual à publicação local"\n'
        "argument-hint: <squad> <pasta da versão, relativa ao squad>\n---\n"
        "1. Rode `python ferramentas/publicar_nuvem.py $ARGUMENTS`. Ele monta `<squad>/publicados/<projeto>/v<n>/` com as mesmas subpastas da publicação local, o `manifesto_publicacao.json` e um zip com tudo.\n"
        "2. Envie com `python ferramentas/drive.py publicar <squad>/publicados/<projeto>/v<n>/manifesto_publicacao.json`. Ele cria só as pastas que faltam em `pasta_drive`, envia todos os arquivos do manifesto e o próprio manifesto sem limite de tamanho e sem converter formatos, substitui os de mesmo nome e confere no Drive nomes e tamanhos. Se terminar com pendências, rode de novo uma vez e informe o que continuar faltando.\n"
        "3. Só se o passo 2 sair com código 3 (sem `ACTA_DRIVE_CREDENCIAL`), use o conector do Google Drive: encontre cada nível de `pasta_drive` e crie só o que não existir (nunca pasta duplicada); envie **todos** os arquivos de `arquivos`, recriando as subpastas, mais o `manifesto_publicacao.json`, com o tipo do manifesto e `disableConversionToGoogleType`; substitua os de mesmo nome e caminho.\n"
        "4. Pelo conector, arquivos acima de 10 MB costumam falhar. Não insista: liste nome e tamanho como pendência, diga que eles estão no zip e no commit de `publicados/`, e lembre Marcus de configurar `ACTA_DRIVE_CREDENCIAL` (NUVEM.md, Arquivos grandes).\n"
        "5. Pelo conector, confira: liste cada pasta no Drive e compare nomes e quantidades com o manifesto. Reenvie o que faltar, no máximo duas tentativas por arquivo.\n"
        "6. Faça commit e push de `<squad>/publicados/` na branch da sessão.\n"
        "7. Responda com o link da pasta da versão no Drive, o total enviado por subpasta e qualquer pendência.\n")
    for rel in gerar:
        p = RAIZ / rel
        if p.exists() and rel not in antes:
            conflitos.append(rel)
    if conflitos:
        sys.exit("Arquivos já existem e não foram gerados por este script (não vou sobrescrever):\n- " + "\n- ".join(conflitos))
    # settings.json da raiz: mescla
    sp = RAIZ / ".claude" / "settings.json"
    cfg = json.loads(sp.read_text(encoding="utf-8")) if sp.exists() else {}
    perm = cfg.setdefault("permissions", {}); perm["deny"] = sorted(set(perm.get("deny", [])) | deny)
    hook_cmd = "python3 ferramentas/preparar_nuvem.py"
    ss = cfg.setdefault("hooks", {}).setdefault("SessionStart", [])
    if not any(h.get("command") == hook_cmd for e in ss for h in e.get("hooks", [])):
        ss.append({"matcher": "startup|resume", "hooks": [{"type": "command", "command": hook_cmd, "timeout": 900}]})
    # CLAUDE.md da raiz: bloco gerenciado
    linhas = ["<!-- squads:inicio (gerado por ferramentas/montar_nuvem.py; não edite à mão) -->", "## Squads da Acta", "",
              "| Squad | Pasta | Prefixo dos agentes | Comandos | Pasta no Drive |", "|---|---|---|---|---|"]
    linhas += [f"| {NOMES.get(n, n)} | `{n}/` | `{p}-` | {', '.join(c)} | {(destinos.get(n) or {}).get('drive', '[●]')} |" for n, p, _, c in resumo]
    linhas += ["", "Regras para todos os squads, em especial na nuvem:",
               "- Cada squad tem o seu `CLAUDE.md`, motor e base de conhecimento. Rode os comandos do motor de dentro da pasta do squad (`cd squad-x && python -m motor...`).",
               "- Na nuvem, arquivos de entrada vêm do Google Drive: baixe para `<squad>/entrada/<trabalho>/` (fora do git) e importe como no uso local. Use primeiro `python ferramentas/drive.py baixar <link, id ou \"Acta > pasta\"> <squad>/entrada/<trabalho>/`, que não tem limite de tamanho; se ele sair com código 3 (sem credencial), use o conector do Google Drive, que só baixa até 10 MB por arquivo. Arquivo acima de 10 MB sem credencial: não trabalhe com o texto extraído parcial; avise Marcus que falta configurar `ACTA_DRIVE_CREDENCIAL` (NUVEM.md, Arquivos grandes) ou peça o arquivo anexado no chat.",
               "- Ao concluir, os comandos principais dos squads publicam sozinhos; para publicar de novo ou manualmente, use `/publicar-drive <squad> <pasta da versão>`: ele envia ao Drive o pacote completo (documentos finais e metadados: JSON, CSV, planilha, nós, revisões), igual à publicação local, e faz commit de `<squad>/publicados/`. A publicação do próprio squad (`python -m motor.publicar`) só funciona no computador, com a pasta do Drive sincronizada. Nunca commite `projetos/`, `entrada/`, `dados/` nem chaves.",
               "- Dados com informação pessoal ou de cliente (squad de análise) só na nuvem se Marcus autorizar; a opção padrão é rodar no computador dele com Remote Control.",
               "<!-- squads:fim -->"]
    bloco = "\n".join(linhas) + "\n"
    cm = RAIZ / "CLAUDE.md"; txt = cm.read_text(encoding="utf-8") if cm.exists() else "# acta-agentes\n\n"
    txt = re.sub(r"<!-- squads:inicio.*?<!-- squads:fim -->\n?", "", txt, flags=re.S).rstrip() + "\n\n" + bloco
    gi = RAIZ / ".gitignore"; gtxt = gi.read_text(encoding="utf-8") if gi.exists() else ""
    gbloco = ("# squads:inicio (gerado; vale só dentro das pastas squad-*)\n"
              "squad-*/**/dados/\nsquad-*/**/entrada/*\n!squad-*/**/entrada/LEIA.md\nsquad-*/**/projetos/*\n!squad-*/**/projetos/.gitkeep\n"
              "squad-*/**/chave_local.key\nsquad-*/**/*.duckdb\nsquad-*/**/*.duckdb.wal\nsquad-*/**/__pycache__/\n.playwright-mcp/\n# squads:fim\n")
    gtxt = re.sub(r"# squads:inicio.*?# squads:fim\n?", "", gtxt, flags=re.S).rstrip()
    gtxt = gtxt + ("\n\n" if gtxt else "") + gbloco
    if simular:
        print(f"[simulação] {len(gerar)} arquivos em .claude/, settings.json mesclado, bloco no CLAUDE.md e no .gitignore")
    else:
        for rel in antes - set(gerar):
            (RAIZ / rel).unlink(missing_ok=True)
        for rel, conteudo in gerar.items():
            p = RAIZ / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(conteudo, encoding="utf-8")
        sp.parent.mkdir(parents=True, exist_ok=True); sp.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cm.write_text(txt, encoding="utf-8"); gi.write_text(gtxt, encoding="utf-8")
        MANIFESTO.write_text(json.dumps({"arquivos": sorted(gerar)}, ensure_ascii=False, indent=2), encoding="utf-8")
    for n, p, a, c in resumo:
        print(f"{n}: {a} agentes com prefixo {p}-, comandos {', '.join(c)}")
    total = sum(r[2] for r in resumo)
    print(f"Total: {total} agentes. As descrições de todos entram no contexto de cada sessão; mantenha-as curtas.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--simular", action="store_true"); montar(ap.parse_args().simular)
