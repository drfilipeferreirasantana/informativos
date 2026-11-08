"""Monta o site de informativos a partir de conteudo/*.json.

Uso (na pasta do repositório):  python ferramentas/gerar.py

Para cada arquivo de conteudo/ gera:
  posts/SLUG.html                  página do post (padrão em docs/padrao-dos-posts.md)
  imagens/SLUG-capa.jpg            1200x630, aparece ao compartilhar o link (WhatsApp, Facebook)
  imagens/SLUG-instagram.jpg       1080x1350, arte para publicar no Instagram
E refaz index.html, sitemap.xml e robots.txt.

Formato de conteudo/AAAA-MM-DD-slug.json:
{
  "slug": "nome-do-post", "area": "familia", "data": "AAAA-MM-DD",
  "titulo": "Você sabia que ...?", "resumo": "Resposta curta em 1 ou 2 frases.",
  "corpo": "<h2>O que a lei prevê</h2><p>...</p><h2>Na prática</h2><ul><li>...</li></ul>",
  "faq": [["Pergunta?", "Resposta."], ...],
  "base": ["Código Civil, art. ..."],
  "fontes": [["Veículo: título (data)", "https://..."]]
}
"""
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).resolve().parent.parent
BASE = "https://informativos.escritorioferreiraadv.com.br/"
SITE = "https://escritorioferreiraadv.com.br/"
NOME = "Ferreira Advogados"
ADVOGADO = "Filipe Ferreira Santana"
OAB = "OAB/ES 37.159"
ENDERECO = "Av. Prefeito Samuel Batista Cruz, 2832, Centro, Linhares/ES"
EMAIL = "dr.filipeferreirasantana@gmail.com"
TELEFONE = "(27) 99518-7279"
WHATSAPP = "https://wa.me/5527995187279"

AREAS = {
    "familia": "Direito de Família",
    "sucessoes": "Sucessões",
    "trabalhista": "Direito Trabalhista",
    "civil": "Direito Civil",
    "consumidor": "Direito do Consumidor",
    "previdenciario": "Direito Previdenciário",
}
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto",
         "setembro", "outubro", "novembro", "dezembro"]

ICONE_WHATS = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.6-1.2.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1.1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1 .2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>'
ICONE_COMPARTILHAR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/></svg>'

e = html.escape


def data_extenso(iso):
    a, m, d = iso.split("-")
    return f"{int(d)} de {MESES[int(m) - 1]} de {a}"


def palavras(texto_html):
    return len(re.sub(r"<[^>]+>", " ", texto_html).split())


def link_whats(titulo):
    return f'{WHATSAPP}?text={quote(f"Olá! Li o informativo \"{titulo}\" e gostaria de falar com o escritório.")}'


def carregar():
    posts = []
    for arq in sorted((RAIZ / "conteudo").glob("*.json")):
        p = json.loads(arq.read_text(encoding="utf-8"))
        faltam = [k for k in ("slug", "area", "data", "titulo", "resumo", "corpo", "base") if not p.get(k)]
        if faltam:
            sys.exit(f"{arq.name}: faltam os campos {faltam}")
        if p["area"] not in AREAS:
            sys.exit(f"{arq.name}: área '{p['area']}' desconhecida. Use: {', '.join(AREAS)}")
        if "—" in json.dumps(p, ensure_ascii=False) or "–" in json.dumps(p, ensure_ascii=False):
            sys.exit(f"{arq.name}: o texto tem travessão; troque por vírgula, ponto ou dois-pontos")
        p.setdefault("faq", [])
        p.setdefault("fontes", [])
        p["_arquivo"] = arq.name
        posts.append(p)
    # Número do informativo pela ordem de publicação (data e nome do arquivo): o primeiro é o nº 1
    posts.sort(key=lambda p: (p["data"], p["_arquivo"]))
    for n, p in enumerate(posts, 1):
        p["numero"] = n
    # Na lista, o mais recente aparece primeiro
    return posts[::-1]


def cabeca(titulo, descricao, url, base, tipo="website", imagem=None, extra=""):
    imagem = imagem or f"{BASE}assets/emblema-prata.png"
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)}</title>
<meta name="description" content="{e(descricao)}">
<meta name="theme-color" content="#39414a">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(descricao)}">
<meta property="og:type" content="{tipo}">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Informativos {NOME}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{imagem}">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="{base}assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/estilo.css">{extra}
</head>
<body>
<a class="pular" href="#conteudo">Ir para o conteúdo</a>
<header class="topo"><div class="conteudo">
  <a class="marca" href="{base}index.html" aria-label="Informativos da {NOME}">
    <img src="{base}assets/emblema-prata.png" alt="" width="38" height="38">
    <span><b>{NOME}</b><small>Informativos</small></span>
  </a>
  <nav aria-label="Principal">
    <a href="{base}index.html">Todos os informativos</a>
    <a href="{SITE}">Site do escritório</a>
  </nav>
</div></header>
<main id="conteudo">
"""


RODAPE = f"""</main>
<footer class="rodape"><div class="conteudo">
  <div class="grade">
    <div>
      <h3>{NOME}</h3>
      <p>Escritório de Advocacia</p>
      <p>Advogado responsável: {ADVOGADO}, {OAB}</p>
      <p>{ENDERECO}</p>
    </div>
    <div>
      <h3>Contato</h3>
      <ul>
        <li><a href="{SITE}">escritorioferreiraadv.com.br</a></li>
        <li><a href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp {TELEFONE}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      </ul>
    </div>
  </div>
  <p class="legal">Conteúdo de caráter informativo, que não substitui a análise individual de cada situação.</p>
</div></footer>
"""


def cartao(p, base=""):
    return (f'<a class="cartao" data-area="{p["area"]}" href="{base}posts/{p["slug"]}.html">'
            f'<span class="meta"><b class="numero">Nº {p["numero"]}</b> · {AREAS[p["area"]]} · {data_extenso(p["data"])}</span>'
            f'<h2>{e(p["titulo"])}</h2><p>{e(p["resumo"])}</p><span class="ler">Ler o informativo</span></a>')


def relacionados(p, posts):
    outros = [o for o in posts if o["slug"] != p["slug"]]
    mesma = [o for o in outros if o["area"] == p["area"]]
    resto = [o for o in outros if o["area"] != p["area"]]
    return (mesma + resto)[:3]


def pagina_post(p, posts):
    url = f"{BASE}posts/{p['slug']}.html"
    area = AREAS[p["area"]]
    minutos = max(1, round((palavras(p["corpo"]) + sum(palavras(q + r) for q, r in p["faq"])) / 200))
    faq = ""
    if p["faq"]:
        itens = "".join(f"<details><summary>{e(q)}</summary><p>{e(r)}</p></details>" for q, r in p["faq"])
        faq = f'<section class="faq" aria-label="Perguntas frequentes"><h2>Perguntas frequentes</h2>{itens}</section>'
    base_legal = "".join(f"<li>{e(b)}</li>" for b in p["base"])
    fontes = ""
    if p["fontes"]:
        itens = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in p["fontes"])
        fontes = f'<div class="caixa fonte"><p><b>Notícia de referência</b></p><ul>{itens}</ul></div>'
    leia = "".join(cartao(o, "../") for o in relacionados(p, posts))
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "Article", "headline": p["titulo"], "description": p["resumo"],
        "datePublished": p["data"], "inLanguage": "pt-BR", "mainEntityOfPage": url,
        "image": f"{BASE}imagens/{p['slug']}-capa.jpg",
        "author": {"@type": "Person", "name": ADVOGADO, "jobTitle": f"Advogado, {OAB}",
                   "memberOf": "Instituto Brasileiro de Direito de Família (IBDFAM)", "url": SITE},
        "publisher": {"@type": "LegalService", "name": NOME, "url": SITE},
    }, ensure_ascii=False)
    whats = link_whats(p["titulo"])
    compartilhar = f"https://wa.me/?text={quote(p['titulo'] + ' ' + url)}"
    corpo = f"""<article class="artigo"><div class="conteudo"><div class="corpo">
  <p class="migalha"><a href="../index.html">Informativos</a> / {area}</p>
  <span class="rotulo">Informativo nº {p['numero']} · {area}</span>
  <h1>{e(p['titulo'])}</h1>
  <div class="resposta"><b>Resposta curta</b><p>{e(p['resumo'])}</p></div>
  <p class="data"><time datetime="{p['data']}">{data_extenso(p['data'])}</time> · {minutos} min de leitura · Por {ADVOGADO}, {OAB}</p>
{p['corpo'].strip()}
  {faq}
  <div class="caixa"><p><b>Base legal</b></p><ul>{base_legal}</ul></div>
  {fontes}
  <p class="aviso">Texto informativo e em tese. Cada situação depende de análise própria, com base nos documentos e nos fatos do caso.</p>
  <aside class="contato-post" aria-label="Quem escreve e contato do escritório">
    <img src="../assets/advogado.jpg" width="240" height="300" loading="lazy" alt="{ADVOGADO}, advogado do escritório, de terno cinza">
    <div>
      <span class="rotulo">Quem escreve</span>
      <h2>{ADVOGADO}</h2>
      <p class="credenciais">Advogado, {OAB}. Pós-graduação em Direito de Família em curso na FMP. Filiado ao IBDFAM.</p>
      <p>O escritório {NOME} atua em Direito de Família, Sucessões, Direito Trabalhista, Direito Civil, Direito do Consumidor e Direito Previdenciário, com atendimento presencial em Linhares/ES e on-line.</p>
      <p>Para tirar dúvidas sobre este assunto ou agendar um atendimento, o contato é pelo WhatsApp.</p>
      <a class="botao botao-whatsapp" href="{whats}" target="_blank" rel="noopener">{ICONE_WHATS}Conversar pelo WhatsApp</a>
    </div>
  </aside>
  <div class="acoes">
    <a class="botao botao-escuro" href="{compartilhar}" target="_blank" rel="noopener">{ICONE_COMPARTILHAR}Compartilhar no WhatsApp</a>
    <a class="botao botao-contorno" href="../index.html">Ver todos os informativos</a>
  </div>
</div>
  <section class="leia" aria-label="Leia também"><h2>Leia também</h2><div class="lista">{leia}</div></section>
</div></article>
<div class="barra-whats"><a class="botao botao-whatsapp" href="{whats}" target="_blank" rel="noopener">{ICONE_WHATS}Conversar pelo WhatsApp</a></div>
"""
    return (cabeca(f"{p['titulo']} | {NOME}", p["resumo"], url, "../", "article",
                   f"{BASE}imagens/{p['slug']}-capa.jpg", f'\n<script type="application/ld+json">{ld}</script>')
            + corpo + RODAPE + "</body>\n</html>\n")


SCRIPT_LISTA = """<script>
(function () {
  var POR_VEZ = 12, mostrando = POR_VEZ, filtro = '';
  var cartoes = [].slice.call(document.querySelectorAll('.lista .cartao'));
  var mais = document.getElementById('mais');
  function aplicar() {
    var visiveis = cartoes.filter(function (c) { return !filtro || c.dataset.area === filtro; });
    cartoes.forEach(function (c) { c.hidden = true; });
    visiveis.slice(0, mostrando).forEach(function (c) { c.hidden = false; });
    mais.hidden = visiveis.length <= mostrando;
  }
  document.querySelectorAll('[data-filtro]').forEach(function (b) {
    b.addEventListener('click', function () {
      filtro = b.dataset.filtro; mostrando = POR_VEZ;
      document.querySelectorAll('[data-filtro]').forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
      aplicar();
    });
  });
  mais.querySelector('button').addEventListener('click', function () { mostrando += POR_VEZ; aplicar(); });
  aplicar();
})();
</script>"""


def pagina_inicial(posts):
    usadas = [k for k in AREAS if any(p["area"] == k for p in posts)]
    botoes = '<button type="button" data-filtro="" aria-pressed="true">Todos</button>' + "".join(
        f'<button type="button" data-filtro="{k}" aria-pressed="false">{AREAS[k]}</button>' for k in usadas)
    cartoes = "\n".join("  " + cartao(p) for p in posts)
    corpo = f"""<section class="abertura"><div class="conteudo">
  <span class="rotulo">Informativos</span>
  <h1>Você sabia?</h1>
  <p>Textos curtos sobre direitos e regras que costumam gerar dúvidas, nas áreas de atuação do escritório.</p>
</div></section>
<section class="conteudo">
  <div class="filtros" role="group" aria-label="Filtrar por área">{botoes}</div>
  <div class="lista">
{cartoes}
  </div>
  <div class="mais" id="mais"><button class="botao botao-contorno" type="button">Ver mais informativos</button></div>
</section>
"""
    return (cabeca(f"Você sabia? Informativos | {NOME}",
                   "Informativos da Ferreira Advogados sobre Direito de Família, Sucessões, Trabalhista, Civil, Consumidor e Previdenciário.",
                   BASE, "") + corpo + RODAPE + SCRIPT_LISTA + "\n</body>\n</html>\n")


# ---------- imagens ----------
FONTES_WIN = Path("C:/Windows/Fonts")


def fonte(nome, tamanho):
    from PIL import ImageFont
    for arq in (FONTES_WIN / nome, Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")):
        if arq.exists():
            return ImageFont.truetype(str(arq), tamanho)
    return ImageFont.load_default(tamanho)


def quebrar(desenho, texto, f, largura):
    linhas, atual = [], ""
    for palavra in texto.split():
        teste = (atual + " " + palavra).strip()
        if desenho.textlength(teste, font=f) <= largura:
            atual = teste
        else:
            linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas


def fundo(l, a):
    from PIL import Image
    img = Image.new("RGB", (l, a), "#39414a")
    topo, fim = (51, 58, 66), (93, 107, 115)
    px = img.load()
    for y in range(a):
        for x in range(0, l):
            t = (x / l * 0.55 + y / a * 0.45)
            px[x, y] = tuple(int(topo[i] + (fim[i] - topo[i]) * t) for i in range(3))
    return img


def imagem(p, l, a, destino, instagram):
    from PIL import Image, ImageDraw
    img = fundo(l, a)
    d = ImageDraw.Draw(img)
    m = int(l * 0.075)
    emblema = Image.open(RAIZ / "assets" / "emblema-prata.png").convert("RGBA")
    lado = int(l * (0.085 if instagram else 0.07))
    img.paste(emblema.resize((lado, lado)), (m, m), emblema.resize((lado, lado)))
    f_marca = fonte("segoeuib.ttf", int(l * 0.026))
    f_sub = fonte("segoeui.ttf", int(l * 0.017))
    d.text((m + lado + int(l * 0.02), m + int(lado * 0.12)), NOME.upper(), font=f_marca, fill="#f6f4f1")
    d.text((m + lado + int(l * 0.02), m + int(lado * 0.58)), "ESCRITÓRIO DE ADVOCACIA", font=f_sub, fill="#d6d9da")
    y = m + lado + int(a * (0.09 if instagram else 0.07))
    f_rot = fonte("segoeuib.ttf", int(l * (0.03 if instagram else 0.022)))
    rotulo = f"VOCÊ SABIA?  ·  {AREAS[p['area']].upper()}"
    d.text((m, y), rotulo, font=f_rot, fill="#c9cdd0")
    y += int(f_rot.size * 1.9)
    largura = l - 2 * m
    f_rod = fonte("segoeui.ttf", int(l * (0.024 if instagram else 0.02)))
    limite = a - m - int(f_rod.size * 3.4)  # o título nunca invade o rodapé
    if instagram:
        limite -= 330  # espaço do traço e da resposta curta
        tamanhos = [88, 80, 72, 64, 58, 52]
    else:
        tamanhos = [64, 58, 52, 46, 42, 38, 34]
    for t in tamanhos:
        f_tit = fonte("segoeuib.ttf", t)
        linhas = quebrar(d, p["titulo"], f_tit, largura)
        if y + len(linhas) * int(t * 1.18) <= limite:
            break
    for linha in linhas:
        d.text((m, y), linha, font=f_tit, fill="#ffffff")
        y += int(t * 1.18)
    if instagram:
        y += int(t * 0.5)
        d.line((m, y, m + int(l * 0.18), y), fill="#a8a8a8", width=4)
        y += int(l * 0.04)
        f_res = fonte("segoeui.ttf", 40)
        for linha in quebrar(d, p["resumo"], f_res, largura)[:5]:
            d.text((m, y), linha, font=f_res, fill="#e7e3de")
            y += 54
    rodape ="Leia o informativo completo: link na bio" if instagram else "informativos.escritorioferreiraadv.com.br"
    d.text((m, a - m - int(f_rod.size * 2.6)), rodape, font=fonte("segoeuib.ttf", f_rod.size), fill="#f6f4f1")
    d.text((m, a - m - int(f_rod.size * 1.2)), f"Advogado responsável: {ADVOGADO}, {OAB}", font=f_rod, fill="#c9cdd0")
    img.save(destino, "JPEG", quality=86, optimize=True, progressive=True)


def main():
    posts = carregar()
    if not posts:
        sys.exit("Nenhum arquivo em conteudo/. Nada foi alterado.")
    (RAIZ / "posts").mkdir(exist_ok=True)
    (RAIZ / "imagens").mkdir(exist_ok=True)
    for p in posts:
        (RAIZ / "posts" / f"{p['slug']}.html").write_text(pagina_post(p, posts), encoding="utf-8")
        capa = RAIZ / "imagens" / f"{p['slug']}-capa.jpg"
        insta = RAIZ / "imagens" / f"{p['slug']}-instagram.jpg"
        if "--imagens" in sys.argv or not capa.exists() or not insta.exists():
            imagem(p, 1200, 630, capa, False)
            imagem(p, 1080, 1350, insta, True)
    (RAIZ / "index.html").write_text(pagina_inicial(posts), encoding="utf-8")
    urls = [BASE] + [f"{BASE}posts/{p['slug']}.html" for p in posts]
    linhas = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    (RAIZ / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{linhas}\n</urlset>\n',
        encoding="utf-8")
    (RAIZ / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
    nao = cabeca(f"Página não encontrada | {NOME}", "Página não encontrada.", BASE, "/") + """<section class="artigo"><div class="conteudo corpo">
  <span class="rotulo">Erro 404</span><h1>Página não encontrada</h1>
  <p class="lide">O endereço acessado não existe ou mudou de lugar.</p>
  <div class="acoes"><a class="botao botao-escuro" href="/index.html">Ver os informativos</a></div>
</div></section>
""" + RODAPE + "</body>\n</html>\n"
    (RAIZ / "404.html").write_text(nao, encoding="utf-8")
    print(f"{len(posts)} posts gerados.")
    for p in posts[:1]:
        print("Mais recente:", f"{BASE}posts/{p['slug']}.html")


if __name__ == "__main__":
    main()
