"""Acesso direto ao Google Drive pela API, sem o limite de 10 MB do conector.

O conector do Google Drive das sessões só baixa arquivos de até 10 MB e envia o conteúdo dentro da própria chamada
(em base64), o que também trava arquivos grandes na publicação. Este script fala direto com a API do Drive:
baixa em blocos, envia por upload retomável e confere tamanho e checksum. Só usa a biblioteca padrão do Python.

Credencial (uma vez): variável de ambiente ACTA_DRIVE_CREDENCIAL com o JSON
  {"client_id": "...", "client_secret": "...", "refresh_token": "..."}
gerado no computador de Marcus com `python ferramentas/drive.py autorizar <client_secret.json>` (veja NUVEM.md).
Sem a variável, o script avisa e sai com código 3; aí vale o conector, que funciona para arquivos de até 10 MB.

Alvos aceitos: link do Drive, id do arquivo ou caminho de pastas como "Acta > Orçamentos > projeto > v1".

Uso (na raiz do repositório):
  python ferramentas/drive.py testar
  python ferramentas/drive.py listar  "Acta > Fornecedores"
  python ferramentas/drive.py baixar  <alvo> <pasta local>        (arquivo ou pasta inteira, recursivo)
  python ferramentas/drive.py enviar  <arquivo local> <pasta no Drive>   (cria a pasta se faltar; substitui o mesmo nome)
  python ferramentas/drive.py publicar <manifesto_publicacao.json>       (envia o pacote de ferramentas/publicar_nuvem.py)
  python ferramentas/drive.py autorizar <client_secret.json>             (só no computador, com navegador)
"""
import hashlib, json, mimetypes, os, re, ssl, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

API = "https://www.googleapis.com/drive/v3"
UPLOAD = "https://www.googleapis.com/upload/drive/v3/files"
TOKEN_URL = "https://oauth2.googleapis.com/token"
ESCOPO = "https://www.googleapis.com/auth/drive"
PASTA = "application/vnd.google-apps.folder"
ATALHO = "application/vnd.google-apps.shortcut"
EXPORTAR = {  # arquivos nativos do Google viram formato do Office (a API limita a exportação a 10 MB)
    "application/vnd.google-apps.document": (".docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    "application/vnd.google-apps.spreadsheet": (".xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
    "application/vnd.google-apps.presentation": (".pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation"),
    "application/vnd.google-apps.drawing": (".pdf", "application/pdf"),
}
BLOCO = 8 * 1024 * 1024  # múltiplo de 256 KiB, exigido pelo upload retomável
COMUM = {"supportsAllDrives": "true"}
_token = {"valor": None, "expira": 0}


def _ssl():
    for caminho in (os.environ.get("SSL_CERT_FILE"), os.environ.get("REQUESTS_CA_BUNDLE"), "/root/.ccr/ca-bundle.crt"):
        if caminho and Path(caminho).is_file():
            return ssl.create_default_context(cafile=caminho)
    return ssl.create_default_context()


CTX = _ssl()


def _abrir(req, tentativas=4):
    for i in range(tentativas):
        try:
            return urllib.request.urlopen(req, context=CTX, timeout=300)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < tentativas - 1:
                time.sleep(2 ** (i + 1)); continue
            raise
        except urllib.error.URLError:
            if i < tentativas - 1:
                time.sleep(2 ** (i + 1)); continue
            raise


def _credencial():
    bruto = os.environ.get("ACTA_DRIVE_CREDENCIAL", "").strip()
    if not bruto:
        print("Sem credencial: defina ACTA_DRIVE_CREDENCIAL no ambiente de nuvem (veja NUVEM.md, seção Arquivos grandes). "
              "Enquanto isso, use o conector do Google Drive (até 10 MB por arquivo).", file=sys.stderr)
        sys.exit(3)
    try:
        cred = json.loads(bruto)
    except json.JSONDecodeError:
        sys.exit("ACTA_DRIVE_CREDENCIAL não é um JSON válido.")
    if isinstance(cred, dict) and ("installed" in cred or "web" in cred):
        sys.exit("ACTA_DRIVE_CREDENCIAL contém o client_secret.json baixado do Google Cloud, não a autorização. "
                 "No computador, rode `python ferramentas/drive.py autorizar <client_secret.json>` e use a linha JSON "
                 "que ele imprime (com refresh_token) como valor da variável.")
    falta = [k for k in ("client_id", "client_secret", "refresh_token") if not cred.get(k)]
    if falta:
        sys.exit("ACTA_DRIVE_CREDENCIAL sem: " + ", ".join(falta))
    return cred


def token():
    if _token["valor"] and time.time() < _token["expira"] - 60:
        return _token["valor"]
    cred = _credencial()
    corpo = urllib.parse.urlencode({"client_id": cred["client_id"], "client_secret": cred["client_secret"],
                                    "refresh_token": cred["refresh_token"], "grant_type": "refresh_token"}).encode()
    try:
        r = json.load(_abrir(urllib.request.Request(TOKEN_URL, data=corpo)))
    except urllib.error.HTTPError as e:
        sys.exit(f"Falha ao renovar o acesso ao Drive ({e.code}): {e.read().decode(errors='replace')[:300]}. "
                 "Se o refresh token foi revogado ou expirou, gere outro com `python ferramentas/drive.py autorizar`.")
    _token.update(valor=r["access_token"], expira=time.time() + int(r.get("expires_in", 3600)))
    return _token["valor"]


def _req(metodo, url, params=None, dados=None, cab=None):
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    h = {"Authorization": f"Bearer {token()}"}
    h.update(cab or {})
    if isinstance(dados, (dict, list)):
        dados = json.dumps(dados).encode(); h.setdefault("Content-Type", "application/json; charset=UTF-8")
    return urllib.request.Request(url, data=dados, headers=h, method=metodo)


def api(metodo, caminho, params=None, dados=None):
    try:
        with _abrir(_req(metodo, API + caminho, {**COMUM, **(params or {})}, dados)) as r:
            corpo = r.read()
            return json.loads(corpo) if corpo else {}
    except urllib.error.HTTPError as e:
        sys.exit(f"Erro da API do Drive ({e.code}) em {metodo} {caminho}: {e.read().decode(errors='replace')[:400]}")


# ---------- localizar ----------

def _q(texto):
    return texto.replace("\\", "\\\\").replace("'", "\\'")


def filhos(pasta_id, nome=None, so_pastas=False):
    q = [f"'{pasta_id}' in parents", "trashed = false"]
    if nome is not None:
        q.append(f"name = '{_q(nome)}'")
    if so_pastas:
        q.append(f"mimeType = '{PASTA}'")
    itens, pagina = [], None
    while True:
        p = {"q": " and ".join(q), "pageSize": 1000, "includeItemsFromAllDrives": "true", "corpora": "allDrives",
             "fields": "nextPageToken, files(id, name, mimeType, size, md5Checksum, modifiedTime, shortcutDetails)",
             "orderBy": "folder, name"}
        if pagina:
            p["pageToken"] = pagina
        r = api("GET", "/files", p)
        itens += r.get("files", [])
        pagina = r.get("nextPageToken")
        if not pagina:
            return itens


def _pasta_raiz(nome):
    """Primeiro nível de um caminho: Meu Drive, depois qualquer pasta com esse nome (compartilhada ou em drive compartilhado)."""
    achadas = filhos("root", nome, so_pastas=True)
    if not achadas:
        r = api("GET", "/files", {"q": f"name = '{_q(nome)}' and mimeType = '{PASTA}' and trashed = false",
                                  "includeItemsFromAllDrives": "true", "corpora": "allDrives", "pageSize": 50,
                                  "fields": "files(id, name, modifiedTime)"})
        achadas = r.get("files", [])
    return achadas


def _escolher(achados, rotulo):
    if len(achados) > 1:
        achados = sorted(achados, key=lambda f: f.get("modifiedTime", ""), reverse=True)
        print(f"Aviso: {len(achados)} itens chamados '{rotulo}'; usando o modificado mais recentemente ({achados[0]['id']}).",
              file=sys.stderr)
    return achados[0] if achados else None


def partes(caminho):
    return [p.strip() for p in re.split(r"\s*>\s*|/", caminho) if p.strip()]


def resolver(alvo, criar=False):
    """Devolve o id de um link, id ou caminho 'A > B > C'. Com criar=True, cria as pastas que faltarem."""
    m = re.search(r"/(?:file/d|folders|document/d|spreadsheets/d|presentation/d)/([\w-]+)", alvo) or re.search(r"[?&]id=([\w-]+)", alvo)
    if m:
        return m.group(1)
    if ">" not in alvo and "/" not in alvo and re.fullmatch(r"[\w-]{20,}", alvo):
        return alvo
    niveis = partes(alvo)
    atual = None
    for i, nome in enumerate(niveis):
        achados = _pasta_raiz(nome) if i == 0 else filhos(atual, nome)
        item = _escolher(achados, nome)
        if item is None:
            if not criar:
                sys.exit(f"Não encontrei '{nome}' em '{' > '.join(niveis[:i]) or 'Meu Drive'}'.")
            item = api("POST", "/files", {"fields": "id"}, {"name": nome, "mimeType": PASTA, "parents": [atual or "root"]})
            print(f"Criei a pasta {' > '.join(niveis[:i + 1])}", file=sys.stderr)
        atual = item["id"]
    return atual


def meta(file_id):
    m = api("GET", f"/files/{file_id}", {"fields": "id, name, mimeType, size, md5Checksum, shortcutDetails, webViewLink"})
    if m.get("mimeType") == ATALHO:
        return meta(m["shortcutDetails"]["targetId"])
    return m


# ---------- baixar ----------

def _nome_local(nome):
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", nome).strip() or "sem_nome"


def baixar_arquivo(m, destino_dir):
    destino_dir.mkdir(parents=True, exist_ok=True)
    nome, tipo = _nome_local(m["name"]), m["mimeType"]
    if tipo in EXPORTAR:
        ext, exp = EXPORTAR[tipo]
        alvo = destino_dir / (nome if nome.lower().endswith(ext) else nome + ext)
        req = _req("GET", f"{API}/files/{m['id']}/export", {"mimeType": exp})
    elif tipo.startswith("application/vnd.google-apps."):
        print(f"Pulando {m['name']}: tipo nativo do Google sem exportação ({tipo}).", file=sys.stderr)
        return None
    else:
        alvo = destino_dir / nome
        req = _req("GET", f"{API}/files/{m['id']}", {**COMUM, "alt": "media", "acknowledgeAbuse": "false"})
    h, total = hashlib.md5(), 0
    parcial = alvo.with_name(alvo.name + ".parcial")
    try:
        with _abrir(req) as r, open(parcial, "wb") as f:
            for bloco in iter(lambda: r.read(1 << 20), b""):
                f.write(bloco); h.update(bloco); total += len(bloco)
    except urllib.error.HTTPError as e:
        parcial.unlink(missing_ok=True)
        msg = e.read().decode(errors="replace")[:300]
        if "exportSizeLimitExceeded" in msg:
            sys.exit(f"{m['name']}: arquivo nativo do Google acima de 10 MB não pode ser exportado pela API. "
                     "No Drive, use Arquivo > Fazer download (.docx/.xlsx/.pdf), suba o arquivo baixado e baixe esse.")
        sys.exit(f"Erro ao baixar {m['name']} ({e.code}): {msg}")
    if m.get("size") and int(m["size"]) != total:
        parcial.unlink(missing_ok=True); sys.exit(f"{m['name']}: baixei {total} bytes, o Drive informa {m['size']}.")
    if m.get("md5Checksum") and m["md5Checksum"] != h.hexdigest():
        parcial.unlink(missing_ok=True); sys.exit(f"{m['name']}: checksum diferente do Drive; tente de novo.")
    parcial.replace(alvo)
    print(f"{alvo}  ({total / 1e6:.1f} MB)")
    return alvo


def baixar(alvo, destino):
    m = meta(resolver(alvo))
    destino = Path(destino)
    if m["mimeType"] != PASTA:
        return [baixar_arquivo(m, destino)]
    feitos, pilha = [], [(m["id"], destino / _nome_local(m["name"]))]
    while pilha:
        pid, local = pilha.pop()
        for f in filhos(pid):
            if f["mimeType"] == ATALHO:
                f = meta(f["shortcutDetails"]["targetId"])
            if f["mimeType"] == PASTA:
                pilha.append((f["id"], local / _nome_local(f["name"])))
            else:
                feitos.append(baixar_arquivo(f, local))
    print(f"Total: {len([f for f in feitos if f])} arquivos em {destino}")
    return feitos


# ---------- enviar ----------

def enviar_arquivo(local, pasta_id, tipo=None, existentes=None):
    local = Path(local)
    tipo = tipo or mimetypes.guess_type(local.name)[0] or "application/octet-stream"
    tamanho = local.stat().st_size
    if existentes is None:
        existentes = {f["name"]: f for f in filhos(pasta_id, local.name)}
    anterior = existentes.get(local.name)
    if anterior:  # substitui o conteúdo e mantém o mesmo arquivo (e o link) no Drive
        url, metodo, metadados = f"{UPLOAD}/{anterior['id']}", "PATCH", {}
    else:
        url, metodo, metadados = UPLOAD, "POST", {"name": local.name, "parents": [pasta_id], "mimeType": tipo}
    ini = _req(metodo, url, {**COMUM, "uploadType": "resumable", "fields": "id, size, md5Checksum"}, metadados,
               {"X-Upload-Content-Type": tipo, "X-Upload-Content-Length": str(tamanho)})
    with _abrir(ini) as r:
        sessao = r.headers["Location"]
    h, enviado, resp = hashlib.md5(), 0, None
    with open(local, "rb") as f:
        while True:
            bloco = f.read(BLOCO)
            h.update(bloco)
            fim = enviado + len(bloco) - 1
            faixa = f"bytes {enviado}-{fim}/{tamanho}" if bloco else f"bytes */{tamanho}"
            req = urllib.request.Request(sessao, data=bloco, method="PUT",
                                         headers={"Content-Length": str(len(bloco)), "Content-Range": faixa})
            try:
                with _abrir(req) as r:
                    resp = json.loads(r.read() or b"{}")
                    break
            except urllib.error.HTTPError as e:
                if e.code != 308:  # 308 = bloco recebido, mande o próximo
                    sys.exit(f"Erro ao enviar {local.name} ({e.code}): {e.read().decode(errors='replace')[:300]}")
                enviado = fim + 1
    if resp.get("md5Checksum") and resp["md5Checksum"] != h.hexdigest():
        sys.exit(f"{local.name}: checksum no Drive diferente do arquivo local.")
    print(f"{'substituído' if anterior else 'enviado'}: {local.name} ({tamanho / 1e6:.1f} MB)")
    return resp


def enviar(local, pasta):
    return enviar_arquivo(local, resolver(pasta, criar=True))


def publicar(manifesto_path):
    manifesto_path = Path(manifesto_path)
    man = json.loads(manifesto_path.read_text(encoding="utf-8"))
    base = manifesto_path.parent
    raiz_id = resolver(man["pasta_drive"], criar=True)
    pastas = {"": raiz_id}

    def pasta_de(sub):
        if sub not in pastas:
            pai, _, nome = sub.rpartition("/")
            pid = pasta_de(pai)
            achada = _escolher(filhos(pid, nome, so_pastas=True), nome)
            pastas[sub] = achada["id"] if achada else api("POST", "/files", {"fields": "id"},
                                                          {"name": nome, "mimeType": PASTA, "parents": [pid]})["id"]
        return pastas[sub]

    itens = man["arquivos"] + [{"caminho": manifesto_path.name, "tipo": "application/json"}]
    por_pasta = {}
    for i in itens:
        sub = i["caminho"].rpartition("/")[0]
        por_pasta.setdefault(sub, []).append(i)
    falhas = []
    for sub, lista in sorted(por_pasta.items()):
        pid = pasta_de(sub)
        existentes = {f["name"]: f for f in filhos(pid)}
        for i in lista:
            try:
                enviar_arquivo(base / i["caminho"], pid, i.get("tipo"), existentes)
            except SystemExit as e:
                falhas.append(f"{i['caminho']}: {e}")
    # conferência: tudo o que está no manifesto precisa estar no Drive com o mesmo tamanho
    faltando = []
    for sub, lista in sorted(por_pasta.items()):
        no_drive = {f["name"]: f for f in filhos(pastas[sub])}
        for i in lista:
            nome = i["caminho"].rpartition("/")[2]
            tam = (base / i["caminho"]).stat().st_size
            if nome not in no_drive or int(no_drive[nome].get("size", -1)) != tam:
                faltando.append(i["caminho"])
    print(f"\nPasta no Drive: {man['pasta_drive']}")
    print(f"Link: https://drive.google.com/drive/folders/{raiz_id}")
    print("Por pasta: " + ", ".join(f"{s or '(raiz)'}: {len(l)}" for s, l in sorted(por_pasta.items())))
    if falhas or faltando:
        print("Pendências:\n- " + "\n- ".join(falhas + [f"não conferiu no Drive: {c}" for c in faltando]))
        sys.exit(1)
    print(f"Conferido: {len(itens)} arquivos no Drive, tamanhos iguais aos locais.")


# ---------- utilitários ----------

def listar(alvo):
    for f in filhos(resolver(alvo)):
        tam = f"{int(f['size']) / 1e6:9.1f} MB" if f.get("size") else "    pasta" if f["mimeType"] == PASTA else "   nativo"
        print(f"{tam}  {f['name']}  ({f['id']})")


def testar():
    r = api("GET", "/about", {"fields": "user(emailAddress, displayName)"})
    print(f"Acesso ao Drive ok: {r['user']['displayName']} <{r['user']['emailAddress']}>")


def autorizar(client_secret):
    """Roda no computador: abre o navegador, recebe a autorização e imprime o JSON para ACTA_DRIVE_CREDENCIAL."""
    import http.server, secrets, webbrowser
    dados = json.loads(Path(client_secret).read_text(encoding="utf-8"))
    dados = dados.get("installed") or dados.get("web") or dados
    estado, recebido = secrets.token_urlsafe(16), {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if q.get("state", [""])[0] == estado:
                recebido.update({k: v[0] for k, v in q.items()})
            self.send_response(200); self.send_header("Content-Type", "text/plain; charset=utf-8"); self.end_headers()
            self.wfile.write("Autorização recebida. Pode fechar esta aba.".encode())

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    redirect = f"http://127.0.0.1:{srv.server_port}"
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": dados["client_id"], "redirect_uri": redirect, "response_type": "code", "scope": ESCOPO,
        "access_type": "offline", "prompt": "consent", "state": estado})
    print("Abrindo o navegador para autorizar o acesso ao Drive. Se não abrir, copie este endereço:\n" + url)
    webbrowser.open(url)
    while "code" not in recebido and "error" not in recebido:
        srv.handle_request()
    if "error" in recebido:
        sys.exit("Autorização recusada: " + recebido["error"])
    corpo = urllib.parse.urlencode({"code": recebido["code"], "client_id": dados["client_id"], "client_secret": dados["client_secret"],
                                    "redirect_uri": redirect, "grant_type": "authorization_code"}).encode()
    r = json.load(urllib.request.urlopen(urllib.request.Request(TOKEN_URL, data=corpo), context=CTX))
    if not r.get("refresh_token"):
        sys.exit("O Google não devolveu refresh token. Remova o acesso do app em myaccount.google.com/permissions e rode de novo.")
    print("\nCopie a linha abaixo inteira como valor da variável ACTA_DRIVE_CREDENCIAL no ambiente de nuvem (não cole no chat):\n")
    print(json.dumps({"client_id": dados["client_id"], "client_secret": dados["client_secret"], "refresh_token": r["refresh_token"]}))


if __name__ == "__main__":
    cmds = {"testar": (testar, 0), "listar": (listar, 1), "baixar": (baixar, 2), "enviar": (enviar, 2),
            "publicar": (publicar, 1), "autorizar": (autorizar, 1)}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds or len(sys.argv) - 2 != cmds[sys.argv[1]][1]:
        sys.exit(__doc__)
    cmds[sys.argv[1]][0](*sys.argv[2:])
