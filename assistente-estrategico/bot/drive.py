#!/usr/bin/env python3
"""drive.py — leitura dos briefings e do planejamento no Google Drive.

Fora das rotinas do Claude Code (que têm conector Google Drive nativo), o bot
em tempo real acessa o Drive por uma SERVICE ACCOUNT do Google Cloud com
permissão de LEITURA na pasta Acta/ (compartilhe a pasta com o e-mail da
service account). Somente leitura — o scope usado é drive.readonly.

Variáveis de ambiente:
  GOOGLE_SERVICE_ACCOUNT_FILE  caminho do JSON da service account (obrigatória)
  DRIVE_DOC_PLANEJAMENTO       nome exato do doc de planejamento (opcional)

Uso:
  python3 drive.py listar [n]          n briefings mais recentes (padrão 5) — JSON id/nome/data
  python3 drive.py ler <file_id>       conteúdo do doc em texto puro
  python3 drive.py buscar "<termo>"    docs da conta cujo texto contém o termo — JSON
  python3 drive.py planejamento        conteúdo do doc de planejamento estratégico
"""
import json
import os
import sys

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
PREFIXO_BRIEFING = "Briefing Inteligencia Acta"
MIME_DOC = "application/vnd.google-apps.document"


def _svc():
    caminho = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE")
    if not caminho or not os.path.exists(caminho):
        sys.exit(
            "GOOGLE_SERVICE_ACCOUNT_FILE não definida ou arquivo inexistente — "
            "acesso ao Drive indisponível; declare a lacuna na resposta."
        )
    creds = service_account.Credentials.from_service_account_file(caminho, scopes=SCOPES)
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def _listar(svc, q: str, n: int, ordem: str = "name desc") -> list[dict]:
    resp = (
        svc.files()
        .list(q=q, orderBy=ordem, pageSize=n, fields="files(id,name,modifiedTime)")
        .execute()
    )
    return resp.get("files", [])


def _exportar(svc, file_id: str) -> str:
    dados = svc.files().export(fileId=file_id, mimeType="text/plain").execute()
    return dados.decode("utf-8", errors="replace") if isinstance(dados, bytes) else str(dados)


def listar(n: int = 5) -> None:
    svc = _svc()
    q = f"name contains '{PREFIXO_BRIEFING}' and mimeType='{MIME_DOC}' and trashed=false"
    print(json.dumps(_listar(svc, q, n), ensure_ascii=False, indent=2))


def ler(file_id: str) -> None:
    print(_exportar(_svc(), file_id))


def buscar(termo: str, n: int = 10) -> None:
    svc = _svc()
    termo_seguro = termo.replace("'", "\\'")
    q = f"fullText contains '{termo_seguro}' and mimeType='{MIME_DOC}' and trashed=false"
    print(json.dumps(_listar(svc, q, n, ordem="modifiedTime desc"), ensure_ascii=False, indent=2))


def planejamento() -> None:
    svc = _svc()
    nome = os.environ.get("DRIVE_DOC_PLANEJAMENTO")
    if nome:
        nome_seguro = nome.replace("'", "\\'")
        q = f"name = '{nome_seguro}' and mimeType='{MIME_DOC}' and trashed=false"
    else:
        q = f"name contains 'Planejamento Estratégico' and mimeType='{MIME_DOC}' and trashed=false"
    docs = _listar(svc, q, 1, ordem="modifiedTime desc")
    if not docs:
        sys.exit(
            "Documento de planejamento estratégico não encontrado no Drive — "
            "responda sem o plano formal e sinalize isso."
        )
    print(f"# {docs[0]['name']} (modificado em {docs[0]['modifiedTime']})\n")
    print(_exportar(svc, docs[0]["id"]))


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    cmd = args[0]
    if cmd == "listar":
        listar(int(args[1]) if len(args) > 1 else 5)
    elif cmd == "ler" and len(args) > 1:
        ler(args[1])
    elif cmd == "buscar" and len(args) > 1:
        buscar(args[1], int(args[2]) if len(args) > 2 else 10)
    elif cmd == "planejamento":
        planejamento()
    else:
        sys.exit(__doc__)
