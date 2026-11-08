"""Monta o site de informativos a partir de conteudo/*.json.

Uso (na pasta do repositório):  python ferramentas/gerar.py          (gera só as imagens que faltam)
                                python ferramentas/gerar.py --imagens (refaz todas as imagens)

Para cada arquivo de conteudo/ gera:
  posts/SLUG.html                  página do post, no padrão visual de docs/padrao-dos-posts.md
  imagens/SLUG-capa.jpg            1200x630, aparece ao compartilhar o link (WhatsApp, Facebook)
  imagens/SLUG-instagram.jpg       1080x1350, arte para publicar no Instagram
E refaz index.html, sitemap.xml, robots.txt e 404.html.

Formato de conteudo/AAAA-MM-DD-slug.json:
{
  "slug": "nome-do-post", "area": "familia", "data": "AAAA-MM-DD",
  "titulo": "Você sabia que ...?",
  "resumo": "A resposta em 1 ou 2 frases.",
  "destaque": "PRAZO: 7 DIAS",                       (até 22 caracteres, em maiúsculas)
  "pontos": [["icone", "frase curta"], [..], [..]],  (exatamente 3; ícones na lista ICONES abaixo)
  "exemplo": "Imagine: ...",                         (situação fictícia do dia a dia, 2 ou 3 frases)
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
ASSINATURA = "Dr. Filipe Ferreira"
OAB = "OAB/ES 37.159"
ENDERECO = "Av. Prefeito Samuel Batista Cruz, 2832, Centro, Linhares/ES"
EMAIL = "dr.filipeferreirasantana@gmail.com"
TELEFONE = "(27) 99518-7279"
WHATSAPP = "https://wa.me/5527995187279"
INSTAGRAM = "https://www.instagram.com/dr.filipeferreira"

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

_S = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
ICONES = {
    "casa": f'<svg {_S}><path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/></svg>',
    "filhos": f'<svg {_S}><circle cx="8" cy="6" r="2.5"/><circle cx="16.5" cy="8.5" r="2"/><path d="M4 20v-5a4 4 0 0 1 8 0v5"/><path d="M13.5 20v-3.5a3 3 0 0 1 6 0V20"/></svg>',
    "carteira": f'<svg {_S}><rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18"/><circle cx="16.5" cy="14.5" r="1.2"/></svg>',
    "documento": f'<svg {_S}><path d="M14 3H6v18h12V7z"/><path d="M14 3v4h4"/><path d="M9 12h6M9 16h6"/></svg>',
    "balanca": f'<svg {_S}><path d="M12 4v16M7 20h10M5 7h14"/><path d="m5 7-3 6a3 3 0 0 0 6 0z"/><path d="m19 7-3 6a3 3 0 0 0 6 0z"/></svg>',
    "calendario": f'<svg {_S}><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
    "alerta": f'<svg {_S}><path d="M12 3 2 20h20z"/><path d="M12 10v4M12 17.5v.5"/></svg>',
    "check": f'<svg {_S}><circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/></svg>',
    "relogio": f'<svg {_S}><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "carrinho": f'<svg {_S}><path d="M3 4h2l2.5 11h10L20 8H6.5"/><circle cx="9" cy="19" r="1.5"/><circle cx="17" cy="19" r="1.5"/></svg>',
    "escudo": f'<svg {_S}><path d="M12 3 4 6v6c0 4.5 3.4 8 8 9 4.6-1 8-4.5 8-9V6z"/><path d="m9 12 2 2 4-4"/></svg>',
    "saude": f'<svg {_S}><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/><path d="M12 9v5M9.5 11.5h5"/></svg>',
    "maleta": f'<svg {_S}><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5h6v2M3 13h18"/></svg>',
    "livro": f'<svg {_S}><path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 21V5"/></svg>',
    "predio": f'<svg {_S}><path d="M3 21h18M5 21V8l7-4 7 4v13"/><path d="M9 21v-6h6v6M9 11h.01M15 11h.01"/></svg>',
}
ICONE_WHATS = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.6-1.2.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1.1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1 .2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>'
ICONE_COMPARTILHAR = f'<svg {_S}><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/></svg>'

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
        obrig = ("slug", "area", "data", "titulo", "resumo", "destaque", "pontos", "corpo", "base")
        faltam = [k for k in obrig if not p.get(k)]
        if faltam:
            sys.exit(f"{arq.name}: faltam os campos {faltam}")
        if p["area"] not in AREAS:
            sys.exit(f"{arq.name}: área '{p['area']}' desconhecida. Use: {', '.join(AREAS)}")
        if len(p["pontos"]) != 3 or any(i not in ICONES for i, _ in p["pontos"]):
            sys.exit(f"{arq.name}: 'pontos' precisa de 3 itens com ícones de: {', '.join(ICONES)}")
        if len(p["destaque"]) > 22:
            sys.exit(f"{arq.name}: 'destaque' passa de 22 caracteres")
        texto = json.dumps(p, ensure_ascii=False)
        if "—" in texto or "–" in texto:
            sys.exit(f"{arq.name}: o texto tem travessão; troque por vírgula, ponto ou dois-pontos")
        p.setdefault("faq", [])
        p.setdefault("fontes", [])
        p.setdefault("exemplo", "")
        p["_arquivo"] = arq.name
        posts.append(p)
    # Número do informativo pela ordem de publicação (data e nome do arquivo): o primeiro é o nº 1
    posts.sort(key=lambda p: (p["data"], p["_arquivo"]))
    for n, p in enumerate(posts, 1):
        p["numero"] = n
    return posts[::-1]  # na lista, o mais recente primeiro


def cabeca(titulo, descricao, url, base, tipo="website", imagem=None, extra="", preload=""):
    imagem = imagem or f"{BASE}assets/emblema-prata.png"
    pre = f'\n<link rel="preload" as="image" href="{preload}">' if preload else ""
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)}</title>
<meta name="description" content="{e(descricao)}">
<meta name="theme-color" content="#0f1b2d">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(descricao)}">
<meta property="og:type" content="{tipo}">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Você sabia? com {ASSINATURA}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{imagem}">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="{base}assets/favicon.png">{pre}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/estilo.css">{extra}
</head>
<body>
<a class="pular" href="#conteudo">Ir para o conteúdo</a>
<header class="topo"><div class="conteudo">
  <a class="marca" href="{base}index.html" aria-label="Você sabia? Informativos da {NOME}">
    <img src="{base}assets/emblema-prata.png" alt="" width="34" height="34">
    <span><b>Você sabia?</b><small>{NOME}</small></span>
  </a>
  <nav aria-label="Principal">
    <a href="{base}index.html">Informativos</a>
    <a href="{SITE}">Site do escritório</a>
    <a class="nav-whats" href="{WHATSAPP}" target="_blank" rel="noopener">{ICONE_WHATS}<span>WhatsApp</span></a>
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
        <li><a href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp {TELEFONE}</a></li>
        <li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram @dr.filipeferreira</a></li>
        <li><a href="{SITE}">escritorioferreiraadv.com.br</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      </ul>
    </div>
  </div>
  <p class="legal">Conteúdo de caráter informativo, que não substitui a análise individual de cada situação.</p>
</div></footer>
"""


def assinatura(base, classe="assinatura"):
    return (f'<div class="{classe}"><img src="{base}assets/rosto.jpg" width="56" height="56" alt="">'
            f'<span><b>{ASSINATURA} explica</b><small>Advogado, {OAB}</small></span></div>')


def cartao(p, base=""):
    return (f'<a class="cartao" data-area="{p["area"]}" href="{base}posts/{p["slug"]}.html">'
            f'<span class="cartao-foto"><img src="{base}assets/fotos/{p["area"]}-p.jpg" width="480" height="300" loading="lazy" alt="">'
            f'<b class="numero">Nº {p["numero"]}</b><span class="destaque">{e(p["destaque"])}</span></span>'
            f'<span class="cartao-texto"><span class="meta">{AREAS[p["area"]]}</span>'
            f'<h2>{e(p["titulo"])}</h2>'
            f'<span class="cartao-autor"><img src="{base}assets/rosto.jpg" width="28" height="28" alt="">{ASSINATURA} explica</span></span></a>')


def relacionados(p, posts):
    outros = [o for o in posts if o["slug"] != p["slug"]]
    return ([o for o in outros if o["area"] == p["area"]] + [o for o in outros if o["area"] != p["area"]])[:3]


def pagina_post(p, posts):
    url = f"{BASE}posts/{p['slug']}.html"
    area = AREAS[p["area"]]
    minutos = max(1, round((palavras(p["corpo"]) + sum(palavras(q + r) for q, r in p["faq"])) / 200))
    pontos = "".join(f'<li><span class="icone">{ICONES[i]}</span><b>{n}</b><p>{e(t)}</p></li>'
                     for n, (i, t) in enumerate(p["pontos"], 1))
    exemplo = ""
    if p["exemplo"]:
        exemplo = f"""<section class="exemplo"><div class="conteudo">
  <div class="balao"><span class="rotulo">Situação do dia a dia</span><p>{e(p['exemplo'])}</p>
  <small>Situação fictícia, criada só para explicar o tema.</small></div>
</div></section>"""
    faq = ""
    if p["faq"]:
        itens = "".join(f"<details><summary>{e(q)}</summary><p>{e(r)}</p></details>" for q, r in p["faq"])
        faq = f'<section class="faq"><h2>Perguntas frequentes</h2>{itens}</section>'
    base_legal = "".join(f"<li>{e(b)}</li>" for b in p["base"])
    fontes = ""
    if p["fontes"]:
        itens = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in p["fontes"])
        fontes = f'<div class="caixa fonte"><b>Notícia de referência</b><ul>{itens}</ul></div>'
    leia = "".join(cartao(o, "../") for o in relacionados(p, posts))
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "Article", "headline": p["titulo"], "description": p["resumo"],
        "datePublished": p["data"], "inLanguage": "pt-BR", "mainEntityOfPage": url,
        "image": f"{BASE}imagens/{p['slug']}-capa.jpg",
        "author": {"@type": "Person", "name": ADVOGADO, "jobTitle": f"Advogado, {OAB}",
                   "memberOf": "Instituto Brasileiro de Direito de Família (IBDFAM)", "url": SITE, "sameAs": [INSTAGRAM]},
        "publisher": {"@type": "LegalService", "name": NOME, "url": SITE},
    }, ensure_ascii=False)
    whats = link_whats(p["titulo"])
    compartilhar = f"https://wa.me/?text={quote(p['titulo'] + ' ' + url)}"
    foto = f"../assets/fotos/{p['area']}.jpg"
    corpo = f"""<article>
<header class="capa">
  <img class="capa-foto" src="{foto}" width="1200" height="800" fetchpriority="high" alt="">
  <div class="conteudo">
    <p class="migalha"><a href="../index.html">Informativos</a> / {area}</p>
    <span class="selo">Nº {p['numero']} · {area}</span>
    <h1>{e(p['titulo'])}</h1>
    {assinatura("../")}
  </div>
</header>
<section class="rapida"><div class="conteudo">
  <span class="rotulo">Resposta em 10 segundos</span>
  <strong class="destaque-grande">{e(p['destaque'])}</strong>
  <p>{e(p['resumo'])}</p>
</div></section>
<section class="pontos"><div class="conteudo">
  <h2>Em 3 pontos</h2>
  <ol>{pontos}</ol>
</div></section>
{exemplo}
<section class="detalhes"><div class="conteudo"><div class="corpo">
  <details class="entenda"><summary><span>Entenda melhor</span><small>{minutos} min de leitura</small></summary>
  <div class="texto">{p['corpo'].strip()}</div></details>
  {faq}
  <div class="caixa"><b>Base legal</b><ul>{base_legal}</ul></div>
  {fontes}
  <p class="aviso">Publicado em <time datetime="{p['data']}">{data_extenso(p['data'])}</time>. Texto informativo e em tese. Cada situação depende de análise própria, com base nos documentos e nos fatos do caso.</p>
</div></div></section>
<section class="advogado"><div class="conteudo">
  <img class="advogado-foto" src="../assets/advogado.jpg" width="240" height="300" loading="lazy" alt="{ADVOGADO}, advogado, de terno cinza">
  <div>
    <span class="rotulo">Quem explica</span>
    <h2>{ASSINATURA}</h2>
    <p class="credenciais">{ADVOGADO} · Advogado, {OAB} · Pós-graduação em Direito de Família em curso na FMP · Filiado ao IBDFAM</p>
    <p>O escritório {NOME} atua em Direito de Família, Sucessões, Direito Trabalhista, Direito Civil, Direito do Consumidor e Direito Previdenciário, com atendimento presencial em Linhares/ES e on-line.</p>
    <p>Para tirar dúvidas sobre este assunto ou agendar um atendimento, o contato é pelo WhatsApp.</p>
    <a class="botao botao-whatsapp" href="{whats}" target="_blank" rel="noopener">{ICONE_WHATS}Conversar pelo WhatsApp</a>
    <a class="botao botao-contorno-claro" href="{compartilhar}" target="_blank" rel="noopener">{ICONE_COMPARTILHAR}Enviar este informativo a alguém</a>
  </div>
</div></section>
<section class="leia"><div class="conteudo">
  <h2>Você também pode gostar</h2>
  <div class="lista">{leia}</div>
  <p class="ver-todos"><a class="botao botao-escuro" href="../index.html">Ver todos os informativos</a></p>
</div></section>
</article>
<div class="barra-whats"><a class="botao botao-whatsapp" href="{whats}" target="_blank" rel="noopener">{ICONE_WHATS}Conversar pelo WhatsApp</a></div>
"""
    return (cabeca(f"{p['titulo']} | {ASSINATURA} explica", p["resumo"], url, "../", "article",
                   f"{BASE}imagens/{p['slug']}-capa.jpg", f'\n<script type="application/ld+json">{ld}</script>', foto)
            + corpo + RODAPE + "</body>\n</html>\n")


SCRIPT_LISTA = """<script>
(function () {
  var POR_VEZ = 12, mostrando = POR_VEZ, filtro = '';
  var cartoes = [].slice.call(document.querySelectorAll('#lista .cartao'));
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
  <div class="abertura-texto">
    <span class="rotulo">Informativos</span>
    <h1>Você sabia?</h1>
    <p>Direitos do dia a dia explicados em poucos segundos: família, herança, trabalho, compras e INSS.</p>
    {assinatura("")}
  </div>
  <img class="abertura-foto" src="assets/advogado.jpg" width="240" height="300" alt="{ADVOGADO}, advogado, de terno cinza">
</div></section>
<section class="conteudo vitrine">
  <div class="filtros" role="group" aria-label="Filtrar por área">{botoes}</div>
  <div class="lista" id="lista">
{cartoes}
  </div>
  <div class="mais" id="mais"><button class="botao botao-escuro" type="button">Ver mais informativos</button></div>
</section>
"""
    return (cabeca(f"Você sabia? Informativos com {ASSINATURA} | {NOME}",
                   "Direitos do dia a dia explicados em poucos segundos pelo Dr. Filipe Ferreira, advogado em Linhares/ES.",
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


def rosto_redondo(lado):
    from PIL import Image, ImageDraw
    r = Image.open(RAIZ / "assets" / "rosto.jpg").convert("RGB").resize((lado, lado), Image.LANCZOS)
    m = Image.new("L", (lado * 4, lado * 4), 0)
    ImageDraw.Draw(m).ellipse((0, 0, lado * 4 - 1, lado * 4 - 1), fill=255)
    return r, m.resize((lado, lado), Image.LANCZOS)


def foto_com_degrade(area, l, a, instagram):
    """Instagram: foto viva em cima, escurecendo para o marinho. Capa: foto à direita, marinho à esquerda."""
    from PIL import Image, ImageOps
    base = Image.new("RGB", (l, a), (15, 27, 45))
    foto = ImageOps.fit(Image.open(RAIZ / "assets" / "fotos" / f"{area}.jpg").convert("RGB"), (l, a), Image.LANCZOS)
    foto = Image.blend(foto, Image.new("RGB", (l, a), (12, 20, 34)), 0.12)
    if instagram:
        tira = Image.new("L", (1, a))
        for y in range(a):
            t = y / a
            tira.putpixel((0, y), 255 if t < 0.30 else max(0, int(255 * (1 - (t - 0.30) / 0.30))))
        mascara = tira.resize((l, a))
    else:
        tira = Image.new("L", (l, 1))
        for x in range(l):
            t = x / l
            tira.putpixel((x, 0), 0 if t < 0.38 else min(215, int(215 * (t - 0.38) / 0.30)))
        mascara = tira.resize((l, a))
    base.paste(foto, (0, 0), mascara)
    return base


def imagem(p, l, a, destino, instagram):
    from PIL import ImageDraw
    img = foto_com_degrade(p["area"], l, a, instagram)
    d = ImageDraw.Draw(img)
    m = int(l * 0.07)
    largura = (l - 2 * m) if instagram else int(l * 0.58)
    branco, prata = (255, 255, 255), (217, 191, 140)

    # selo "VOCÊ SABIA?" no alto
    f_selo = fonte("segoeuib.ttf", int(l * (0.032 if instagram else 0.026)))
    texto_selo = f"VOCÊ SABIA?  ·  Nº {p['numero']}"
    w = d.textlength(texto_selo, font=f_selo)
    d.rounded_rectangle((m, m, m + w + f_selo.size * 1.4, m + f_selo.size * 2), radius=f_selo.size, fill=(15, 27, 45), outline=(184, 147, 90), width=3)
    d.text((m + f_selo.size * 0.7, m + f_selo.size * 0.42), texto_selo, font=f_selo, fill=(217, 191, 140))

    # rodapé: rosto + assinatura
    lado = int(l * (0.13 if instagram else 0.085))
    rosto, mascara = rosto_redondo(lado)
    y_rod = a - m - lado
    img.paste(rosto, (m, y_rod), mascara)
    d.ellipse((m - 3, y_rod - 3, m + lado + 3, y_rod + lado + 3), outline=(184, 147, 90), width=5)
    f_ass = fonte("segoeuib.ttf", int(l * (0.036 if instagram else 0.028)))
    f_sub = fonte("segoeui.ttf", int(l * (0.024 if instagram else 0.02)))
    x_ass = m + lado + int(l * 0.025)
    d.text((x_ass, y_rod + lado * 0.12), f"{ASSINATURA} explica", font=f_ass, fill=branco)
    linha2 = f"Advogado, {OAB}" + ("  ·  link na bio" if instagram else "  ·  informativos.escritorioferreiraadv.com.br")
    d.text((x_ass, y_rod + lado * 0.12 + f_ass.size * 1.35), linha2, font=f_sub, fill=prata)

    # destaque (pílula) logo acima do rodapé
    f_dest = fonte("segoeuib.ttf", int(l * (0.042 if instagram else 0.03)))
    wd = d.textlength(p["destaque"], font=f_dest)
    y_dest = y_rod - int(l * (0.06 if instagram else 0.045)) - f_dest.size * 2
    d.rounded_rectangle((m, y_dest, m + wd + f_dest.size * 1.4, y_dest + f_dest.size * 1.9), radius=10, fill=(184, 147, 90))
    d.text((m + f_dest.size * 0.7, y_dest + f_dest.size * 0.38), p["destaque"], font=f_dest, fill=(15, 27, 45))

    # título: o maior tamanho que caiba entre o selo e o destaque
    topo = m + f_selo.size * 2 + int(a * (0.30 if instagram else 0.06))
    limite = y_dest - int(l * 0.035)
    tamanhos = [96, 88, 80, 72, 66, 60, 54] if instagram else [66, 60, 54, 48, 44, 40, 36]
    for t in tamanhos:
        f_tit = fonte("segoeuib.ttf", t)
        linhas = quebrar(d, p["titulo"], f_tit, largura)
        altura = len(linhas) * int(t * 1.16)
        if topo + altura <= limite:
            break
    y = limite - altura if instagram else topo
    for linha in linhas:
        d.text((m + 2, y + 2), linha, font=f_tit, fill=(0, 0, 0))
        d.text((m, y), linha, font=f_tit, fill=branco)
        y += int(t * 1.16)
    img.save(destino, "JPEG", quality=84, optimize=True, progressive=True)


def pagina_artes(posts):
    """Página só para o Dr. Filipe (fora do Google): artes e links prontos para as redes."""
    itens = []
    for p in posts:
        url = f"{BASE}posts/{p['slug']}.html"
        compartilhar = f"https://wa.me/?text={quote(p['titulo'] + ' ' + url + '?v=' + str(p['numero']))}"
        itens.append(f"""<div class="arte">
  <img src="imagens/{p['slug']}-instagram.jpg" width="1080" height="1350" loading="lazy" alt="">
  <div><b>Nº {p['numero']} · {e(p['titulo'])}</b>
  <a class="botao botao-escuro" href="imagens/{p['slug']}-instagram.jpg" download>Baixar arte do Instagram</a>
  <a class="botao botao-escuro" href="imagens/{p['slug']}-capa.jpg" download>Baixar capa (WhatsApp e Facebook)</a>
  <a class="botao botao-whatsapp" href="{compartilhar}" target="_blank" rel="noopener">{ICONE_WHATS}Enviar no WhatsApp</a>
  <a class="botao botao-escuro" href="posts/{p['slug']}.html">Abrir o post</a></div>
</div>""")
    corpo = f"""<section class="artes conteudo">
  <h1>Artes para as redes</h1>
  <p>Página de uso do escritório. Baixe a arte para postar no Instagram ou no Status do WhatsApp, ou envie o link já com a prévia.</p>
  <div class="lista">{"".join(itens)}</div>
</section>
"""
    html_ = cabeca(f"Artes para as redes | {NOME}", "Artes dos informativos para as redes.", f"{BASE}artes.html", "")
    html_ = html_.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex">', 1)
    return html_ + corpo + RODAPE + "</body>\n</html>\n"


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
    (RAIZ / "artes.html").write_text(pagina_artes(posts), encoding="utf-8")
    urls = [BASE] + [f"{BASE}posts/{p['slug']}.html" for p in posts]
    linhas = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    (RAIZ / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{linhas}\n</urlset>\n',
        encoding="utf-8")
    (RAIZ / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
    nao = cabeca(f"Página não encontrada | {NOME}", "Página não encontrada.", BASE, "/") + """<section class="rapida"><div class="conteudo">
  <span class="rotulo">Erro 404</span><strong class="destaque-grande">PÁGINA NÃO ENCONTRADA</strong>
  <p>O endereço acessado não existe ou mudou de lugar.</p>
  <p><a class="botao botao-escuro" href="/index.html">Ver os informativos</a></p>
</div></section>
""" + RODAPE + "</body>\n</html>\n"
    (RAIZ / "404.html").write_text(nao, encoding="utf-8")
    print(f"{len(posts)} posts gerados.")
    print("Mais recente:", f"{BASE}posts/{posts[0]['slug']}.html")


if __name__ == "__main__":
    main()
