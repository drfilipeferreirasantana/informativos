"""Monta o site de informativos a partir de conteudo/*.json.

Uso (na pasta do repositório):  python ferramentas/gerar.py          (gera só as imagens que faltam)
                                python ferramentas/gerar.py --imagens (refaz todas as imagens)

Para cada arquivo de conteudo/ gera:
  posts/SLUG.html                  página do post (padrão em docs/padrao-dos-posts.md)
  imagens/SLUG-capa.jpg            1200x630, prévia do link no WhatsApp e no Facebook
  imagens/SLUG-instagram.jpg       1080x1350, arte para Instagram e Status do WhatsApp
E refaz index.html, artes.html, sitemap.xml, robots.txt e 404.html.

Formato de conteudo/AAAA-MM-DD-slug.json:
{
  "slug": "nome-do-post", "area": "familia", "data": "AAAA-MM-DD",
  "titulo": "A pergunta direta que a pessoa faria?",
  "destaque": "Não automaticamente.",            (a resposta em poucas palavras, frase normal, até 40 caracteres)
  "resumo": "A explicação da resposta em 1 ou 2 frases.",
  "pontos": [["icone", "frase curta"], ...],     (2 a 4 itens; o ícone fica guardado, mas não aparece no visual atual)
  "exemplo": "Ana se separou e ...",             (situação fictícia do dia a dia, 2 ou 3 frases)
  "corpo": "<h2>O que a lei prevê</h2><p>...</p><h2>Na prática</h2><ul><li>...</li></ul>",
  "faq": [["Pergunta?", "Resposta."], ...],
  "base": ["Código Civil, art. ..."],
  "fontes": [["Veículo: título (data)", "https://..."]],
  "foto": {"fonte": "Pexels", "url": "https://www.pexels.com/photo/ID/", "licenca": "https://www.pexels.com/license/"}
}

REGRA DAS FOTOS: cada informativo tem foto própria, ligada ao tema, em assets/fotos/posts/SLUG.jpg (1200x800)
e assets/fotos/posts/SLUG-p.jpg (480x300). O gerador recusa post sem foto, sem o campo "foto" ou com foto
igual à de outro post (mesmo arquivo ou mesma foto do Pexels).

Visual (escolhido pelo Dr. Filipe em 8/11/2026): formato de jornal (foto em cima com borda reta,
linhas finas, rodapé com nome e assinatura) e letras com serifa no título. Papel claro, tinta
quase preta e bordô (a cor da gravata da foto oficial) só nos detalhes. Sem degradês, selos
arredondados ou ícones em círculos.
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
NOME_CURTO = "Filipe Ferreira"
OAB = "OAB/ES 37.159"
ENDERECO = "Av. Prefeito Samuel Batista Cruz, 2832, Centro, Linhares/ES"
EMAIL = "dr.filipeferreirasantana@gmail.com"
TELEFONE = "(27) 99518-7279"
WHATSAPP = "https://wa.me/5527995187279"
# Mensagem do WhatsApp do menu e do rodapé: o sistema do escritório reconhece a frase
WHATS_GERAL = f'{WHATSAPP}?text={quote("Olá! Vim pelo site de informativos e gostaria de falar com o escritório.")}'
INSTAGRAM = "https://www.instagram.com/dr.filipeferreira"
YOUTUBE = "https://www.youtube.com/@Filipeferreiraadvogado"
# Número ISSN concedido pelo IBICT (cbissn.ibict.br). Enquanto vazio, o rodapé não mostra a linha do ISSN.
ISSN = ""

AREAS = {
    "familia": "Direito de Família",
    "sucessoes": "Sucessões",
    "trabalhista": "Direito Trabalhista",
    "civil": "Direito Civil",
    "consumidor": "Direito do Consumidor",
    "previdenciario": "Direito Previdenciário",
}
ICONES = {"casa", "filhos", "carteira", "documento", "balanca", "calendario", "alerta", "check", "relogio",
          "carrinho", "escudo", "saude", "maleta", "livro", "predio"}
SERIES = {
    "motoristas": {
        "titulo": "Direitos do motorista",
        "aba": "Motoristas",
        "pagina": "motoristas.html",
        "descricao": "Informativos sobre os direitos dos motoristas de caminhão e de ônibus de viagem com carteira assinada: jornada, tempo de espera, descanso e descontos, e também as situações graves da estrada, como acidente, assalto, doença de coluna, pensão do INSS e indenização à família.",
    },
}
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto",
         "setembro", "outubro", "novembro", "dezembro"]

ICONE_WHATS = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.6-1.2.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1.1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1 .2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>'

e = html.escape


def versao(caminho):
    """Hash curto do arquivo: muda quando o arquivo muda, e o navegador baixa a versão nova em vez da guardada."""
    import hashlib
    arq = RAIZ / caminho
    return hashlib.md5(arq.read_bytes()).hexdigest()[:8] if arq.exists() else "0"


def volume(iso):
    """Designação numérica exigida pelo ISSN: um volume por ano civil, a partir de 2026."""
    ano = int(iso[:4])
    return f"Vol. {ano - 2025} ({ano})"


def data_curta(iso):
    a, m, d = iso.split("-")
    return f"{int(d)} {MESES[int(m) - 1][:3]}. {a}"


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
        if not 2 <= len(p["pontos"]) <= 4 or any(i not in ICONES for i, _ in p["pontos"]):
            sys.exit(f"{arq.name}: 'pontos' precisa de 2 a 4 itens com ícones de: {', '.join(sorted(ICONES))}")
        if len(p["destaque"]) > 40:
            sys.exit(f"{arq.name}: 'destaque' passa de 40 caracteres")
        texto = json.dumps(p, ensure_ascii=False)
        if "—" in texto or "–" in texto:
            sys.exit(f"{arq.name}: o texto tem travessão; troque por vírgula, ponto ou dois-pontos")
        p.setdefault("faq", [])
        p.setdefault("fontes", [])
        p.setdefault("exemplo", "")
        p.setdefault("serie", "")
        p.setdefault("ordem", 0)
        if p["serie"] and p["serie"] not in SERIES:
            sys.exit(f"{arq.name}: série desconhecida: {p['serie']}")
        p["_arquivo"] = arq.name
        posts.append(p)
    # Regra: cada informativo tem a sua foto, e nenhuma foto se repete
    import hashlib
    vistos_arquivo, vistos_url = {}, {}
    for p in posts:
        for sufixo in ("", "-p"):
            arq = RAIZ / "assets" / "fotos" / "posts" / f"{p['slug']}{sufixo}.jpg"
            if not arq.exists():
                sys.exit(f"{p['_arquivo']}: falta a foto própria do post em {arq.relative_to(RAIZ)}")
        if not (p.get("foto") or {}).get("url"):
            sys.exit(f"{p['_arquivo']}: falta o campo 'foto' com a origem da imagem")
        h = hashlib.md5((RAIZ / "assets" / "fotos" / "posts" / f"{p['slug']}.jpg").read_bytes()).hexdigest()
        u = p["foto"]["url"].rstrip("/").split("/")[-1].split("-")[-1]
        if h in vistos_arquivo or u in vistos_url:
            outro = vistos_arquivo.get(h) or vistos_url.get(u)
            sys.exit(f"{p['_arquivo']}: a foto repete a do post '{outro}'. Cada informativo precisa de foto própria.")
        vistos_arquivo[h] = vistos_url[u] = p["slug"]
    # Número do informativo pela ordem de publicação (data e nome do arquivo): o primeiro é o nº 1
    posts.sort(key=lambda p: (p["data"], p["_arquivo"]))
    for n, p in enumerate(posts, 1):
        p["numero"] = n
    return posts[::-1]  # na lista, o mais recente primeiro


def abas(base):
    return "".join(f'\n    <a href="{base}{s["pagina"]}">{s["aba"]}</a>' for s in SERIES.values())


def cabeca(titulo, descricao, url, base, tipo="website", imagem=None, extra="", preload="", robots=""):
    imagem = imagem or f"{BASE}assets/emblema-prata.png"
    pre = f'\n<link rel="preload" as="image" href="{preload}">' if preload else ""
    rob = '\n<meta name="robots" content="noindex">' if robots else ""
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">{rob}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)}</title>
<meta name="description" content="{e(descricao)}">
<meta name="theme-color" content="#ece7de">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(descricao)}">
<meta property="og:type" content="{tipo}">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Você sabia? | {NOME}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{imagem}">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="{base}assets/favicon.png">{pre}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/estilo.css?v={versao('assets/estilo.css')}">{extra}
</head>
<body>
<a class="pular" href="#conteudo">Ir para o conteúdo</a>
<header class="topo"><div class="conteudo">
  <a class="marca" href="{base}index.html" aria-label="Você sabia? Informativos da {NOME}">
    <b>Você sabia?</b><span>{NOME}</span>
  </a>
  <nav aria-label="Principal">
    <a href="{base}index.html">Informativos</a>{abas(base)}
    <a href="{SITE}">Site do escritório</a>
    <a class="nav-whats" href="{WHATS_GERAL}" target="_blank" rel="noopener">{ICONE_WHATS}<span>WhatsApp</span></a>
  </nav>
</div></header>
<main id="conteudo">
"""


_C = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"'
ICONES_CONTATO = {
    "whatsapp": f'<svg {_C}><path d="M4.2 19.8 5.3 16A8.3 8.3 0 1 1 8.4 19z"/><path d="M9.3 8.6c-.3.9 0 2.1 1 3.3 1.1 1.3 2.4 2 3.4 2 .5 0 .9-.4 1-.8l.1-.5-1.5-.8-.7.6c-.8-.3-1.6-1.1-1.9-1.9l.6-.7-.8-1.5-.5.1c-.3.1-.6.4-.7.7Z" stroke-width="1.2"/></svg>',
    "youtube": f'<svg {_C}><rect x="2.5" y="5.5" width="19" height="13" rx="3.5"/><path d="m10 9.2 5 2.8-5 2.8z"/></svg>',
    "instagram": f'<svg {_C}><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r=".9" fill="currentColor" stroke="none"/></svg>',
    "email": f'<svg {_C}><rect x="3" y="5.5" width="18" height="13" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/></svg>',
    "site": f'<svg {_C}><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3Z"/></svg>',
}


def rodape(base):
    issn = f"\n      <p>ISSN {ISSN}</p>" if ISSN else ""
    contatos = [
        ("whatsapp", WHATS_GERAL, TELEFONE, "WhatsApp", True),
        ("youtube", YOUTUBE, "youtube.com/@Filipeferreiraadvogado", "YouTube", True),
        ("instagram", INSTAGRAM, "@dr.filipeferreira", "Instagram", True),
        ("email", f"mailto:{EMAIL}", EMAIL, "E-mail", False),
        ("site", SITE, "escritorioferreiraadv.com.br", "Site do escritório", False),
    ]
    itens = "".join(
        f'<li><a href="{u}"{" target=\"_blank\" rel=\"noopener\"" if ext else ""} aria-label="{rot}">{ICONES_CONTATO[i]}<span>{txt}</span></a></li>'
        for i, u, txt, rot, ext in contatos)
    return f"""</main>
<footer class="rodape"><div class="conteudo">
  <div class="grade">
    <div class="rodape-logo">
      <img src="{base}assets/emblema-prata.png" width="96" height="96" alt="Logo da {NOME}">
      <b>{NOME}</b><small>Escritório de Advocacia</small>
    </div>
    <div>
      <h3>Você sabia? Informativos {NOME}</h3>{issn}
      <p>Editor responsável: {ADVOGADO}, {OAB}</p>
      <p>{ENDERECO}</p>
      <p class="rodape-links"><a href="{base}apresentacao.html">Apresentação</a> · <a href="{base}volumes.html">Volumes publicados</a> · <a href="{base}expediente.html">Expediente</a></p>
    </div>
    <div>
      <h3>Contato</h3>
      <ul class="contatos">{itens}</ul>
    </div>
  </div>
  <p class="legal">Conteúdo de caráter informativo, que não substitui a análise individual de cada situação.</p>
</div></footer>
<script src="{base}assets/rastreio.js?v={versao('assets/rastreio.js')}" defer></script>
"""


def assinatura(base):
    return (f'<div class="assinatura"><div class="assinatura-linha">'
            f'<img class="assinatura-foto" src="{base}assets/rosto.jpg" width="64" height="64" alt="">'
            f'<span><b>{NOME_CURTO}</b><small>Advogado · {OAB} · Linhares/ES</small></span></div>'
            f'<span class="assinatura-traco" role="img" aria-label="Assinatura de {NOME_CURTO}"></span></div>')


def cartao(p, base=""):
    return (f'<a class="cartao" data-area="{p["area"]}" href="{base}posts/{p["slug"]}.html">'
            f'<img src="{base}assets/fotos/posts/{p["slug"]}-p.jpg" width="480" height="300" loading="lazy" alt="">'
            f'<span class="meta">{AREAS[p["area"]]} · {data_curta(p["data"])}</span>'
            f'<h2>{e(p["titulo"])}</h2>'
            f'<span class="resposta-curta">{e(p["destaque"])}</span></a>')


def link_topo(p):
    if p.get("serie"):
        s = SERIES[p["serie"]]
        return f'<a href="../{s["pagina"]}">Série {s["titulo"]}</a>'
    return '<a href="../index.html">Todos os informativos</a>'


def relacionados(p, posts):
    outros = [o for o in posts if o["slug"] != p["slug"]]
    if p.get("serie"):
        mesma = sorted([o for o in outros if o.get("serie") == p["serie"]], key=lambda o: o["ordem"])
        return ([o for o in mesma if o["ordem"] > p["ordem"]] + [o for o in mesma if o["ordem"] < p["ordem"]])[:3]
    outros = [o for o in outros if not o.get("serie")]
    return ([o for o in outros if o["area"] == p["area"]] + [o for o in outros if o["area"] != p["area"]])[:3]


def pagina_post(p, posts):
    url = f"{BASE}posts/{p['slug']}.html"
    area = AREAS[p["area"]]
    minutos = max(1, round((palavras(p["corpo"]) + sum(palavras(q + r) for q, r in p["faq"])) / 200))
    pontos = "".join(f"<li><p>{e(t)}</p></li>" for _, t in p["pontos"])
    exemplo = ""
    if p["exemplo"]:
        exemplo = f"""<aside class="exemplo"><span class="rotulo">Situação do dia a dia</span>
  <p>{e(p['exemplo'])}</p><small>Situação ilustrativa, com nomes inventados.</small></aside>"""
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
    foto = f"../assets/fotos/posts/{p['slug']}.jpg"
    corpo = f"""<article class="post" data-assunto="{area}">
<div class="conteudo coluna">
  <p class="linha-topo"><b>{area}</b> {volume(p['data'])} · {data_extenso(p['data'])}{link_topo(p)}</p>
  <img class="foto-post" src="{foto}" width="1200" height="800" fetchpriority="high" alt="">
  <h1>{e(p['titulo'])}</h1>
  <div class="resposta"><strong>{e(p['destaque'])}</strong> {e(p['resumo'])}</div>
  <ol class="pontos">{pontos}</ol>
  {exemplo}
  <details class="entenda"><summary>Entenda melhor <small>{minutos} min de leitura</small></summary>
  <div class="texto">{p['corpo'].strip()}</div></details>
  {faq}
  <div class="caixa"><b>Base legal</b><ul>{base_legal}</ul></div>
  {fontes}
  <p class="aviso">Publicado em <time datetime="{p['data']}">{data_extenso(p['data'])}</time>. Texto informativo e em tese. Cada situação depende de análise própria, com base nos documentos e nos fatos do caso.</p>
  <section class="autor">
    <img class="autor-foto" src="../assets/advogado.jpg" width="240" height="300" loading="lazy" alt="{ADVOGADO}, advogado, de terno cinza e gravata bordô">
    <div>
      <span class="rotulo">Quem escreve</span>
      <h2>{NOME_CURTO}</h2>
      <p class="credenciais">{ADVOGADO}, advogado, {OAB}. Pós-graduação em Direito de Família em curso na FMP. Filiado ao IBDFAM.</p>
      <p>O escritório {NOME} atua em Direito de Família, Sucessões, Direito Trabalhista, Direito Civil, Direito do Consumidor e Direito Previdenciário, com atendimento presencial em Linhares/ES e on-line.</p>
      <p>Para tirar dúvidas sobre este assunto ou agendar um atendimento, o contato é pelo WhatsApp.</p>
      <span class="assinatura-traco autor-assinatura" role="img" aria-label="Assinatura de {NOME_CURTO}"></span>
      <p class="acoes"><a class="botao botao-whatsapp" href="{whats}" target="_blank" rel="noopener">{ICONE_WHATS}Conversar pelo WhatsApp</a>
      <a class="botao botao-linha" href="{compartilhar}" target="_blank" rel="noopener">Enviar este informativo a alguém</a></p>
    </div>
  </section>
</div>
<section class="leia"><div class="conteudo">
  <h2>Leia também</h2>
  <div class="lista">{leia}</div>
  <p class="ver-todos"><a class="botao botao-linha" href="../index.html">Ver todos os informativos</a></p>
</div></section>
</article>
<div class="barra-whats"><a class="botao botao-whatsapp" href="{whats}" target="_blank" rel="noopener">{ICONE_WHATS}Conversar pelo WhatsApp</a></div>
"""
    return (cabeca(f"{p['titulo']} | {NOME_CURTO}, advogado", p["resumo"], url, "../", "article",
                   f"{BASE}imagens/{p['slug']}-capa.jpg?v={versao('imagens/' + p['slug'] + '-capa.jpg')}",
                   f'\n<script type="application/ld+json">{ld}</script>', foto)
            + corpo + rodape("../") + "</body>\n</html>\n")


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


def destaques_series(posts):
    blocos = []
    for k, s in SERIES.items():
        n = sum(1 for p in posts if p.get("serie") == k)
        if n:
            blocos.append(f'''<a class="serie-destaque" href="{s["pagina"]}"><span class="rotulo">Série · {n} informativos</span>
    <b>{s["titulo"]}</b><span class="desc">{s["descricao"]}</span><span class="ver">Ver a série</span></a>''')
    return "".join(blocos)


def pagina_inicial(todos):
    destaques = destaques_series(todos)
    posts = [p for p in todos if not p.get("serie")]
    usadas = [k for k in AREAS if any(p["area"] == k for p in posts)]
    botoes = '<button type="button" data-filtro="" aria-pressed="true">Todos</button>' + "".join(
        f'<button type="button" data-filtro="{k}" aria-pressed="false">{AREAS[k]}</button>' for k in usadas)
    cartoes = "\n".join("  " + cartao(p) for p in posts)
    corpo = f"""<section class="abertura"><div class="conteudo">
  <div>
    <p class="linha-topo"><b>Informativos</b> {NOME}</p>
    <h1>Você sabia?</h1>
    <p class="chamada">Dúvidas comuns sobre família, herança, trabalho, compras e INSS, respondidas de forma direta.</p>
    {assinatura("")}
  </div>
</div></section>
<section class="conteudo vitrine">
  {destaques}
  <div class="filtros" role="group" aria-label="Filtrar por área">{botoes}</div>
  <div class="lista" id="lista">
{cartoes}
  </div>
  <div class="mais" id="mais"><button class="botao botao-linha" type="button">Ver mais informativos</button></div>
</section>
"""
    return (cabeca(f"Você sabia? Informativos de {NOME_CURTO} | {NOME}",
                   "Dúvidas comuns sobre família, herança, trabalho, compras e INSS, respondidas por Filipe Ferreira, advogado em Linhares/ES.",
                   BASE, "") + corpo + rodape("") + SCRIPT_LISTA + "\n</body>\n</html>\n")


def pagina_artes(posts):
    """Página só para o Dr. Filipe (fora do Google): artes e links prontos para as redes."""
    itens = []
    for p in posts:
        vi = versao('imagens/' + p['slug'] + '-instagram.jpg')
        vc = versao('imagens/' + p['slug'] + '-capa.jpg')
        url = f"{BASE}posts/{p['slug']}.html"
        compartilhar = f"https://wa.me/?text={quote(p['titulo'] + ' ' + url + '?v=' + str(p['numero']))}"
        itens.append(f"""<div class="arte">
  <img src="imagens/{p['slug']}-instagram.jpg?v={vi}" width="1080" height="1350" loading="lazy" alt="">
  <div><b>{e(p['titulo'])}</b>
  <a class="botao botao-linha" href="imagens/{p['slug']}-instagram.jpg?v={vi}" download>Baixar arte do Instagram</a>
  <a class="botao botao-linha" href="imagens/{p['slug']}-capa.jpg?v={vc}" download>Baixar capa (WhatsApp e Facebook)</a>
  <a class="botao botao-whatsapp" href="{compartilhar}" target="_blank" rel="noopener">{ICONE_WHATS}Enviar no WhatsApp</a>
  <a class="botao botao-linha" href="posts/{p['slug']}.html">Abrir o post</a></div>
</div>""")
    corpo = f"""<section class="artes conteudo">
  <h1>Artes para as redes</h1>
  <p>Página de uso do escritório. Baixe a arte para postar no Instagram ou no Status do WhatsApp, ou envie o link já com a prévia.</p>
  <div class="lista">{"".join(itens)}</div>
</section>
"""
    return (cabeca(f"Artes para as redes | {NOME}", "Artes dos informativos para as redes.", f"{BASE}artes.html", "", robots=True)
            + corpo + rodape("") + "</body>\n</html>\n")


# ---------- imagens ----------
FONTES_WIN = "C:/Windows/Fonts/"
PAPEL, TINTA, BORDO, CINZA = (236, 231, 222), (22, 22, 22), (122, 35, 51), (74, 74, 74)


def fonte(arq, tamanho, estilo=None):
    from PIL import ImageFont
    try:
        f = ImageFont.truetype(FONTES_WIN + arq, tamanho)
        if estilo:
            f.set_variation_by_name(estilo)
        return f
    except OSError:
        return ImageFont.load_default(tamanho)


def serifa(t, estilo="Display Bold"):
    return fonte("SitkaVF.ttf", t, estilo)


def condensada(t, estilo="SemiCondensed"):
    return fonte("bahnschrift.ttf", t, estilo)


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


def escrever(d, x, y, linhas, f, cor, entre):
    for linha in linhas:
        d.text((x, y), linha, font=f, fill=cor)
        y += int(f.size * entre)
    return y


def titulo_que_cabe(d, texto, largura, altura, tamanhos, entre=1.08):
    for t in tamanhos:
        f = serifa(t)
        linhas = quebrar(d, texto, f, largura)
        if len(linhas) * int(t * entre) <= altura:
            return f, linhas
    return f, linhas


def rodape_imagem(img, d, m, y, l, foto_lado, f_nome, f_sub, assinatura_alt):
    from PIL import Image, ImageOps
    d.line((m, y, l - m, y), fill=TINTA, width=2)
    adv = Image.open(RAIZ / "assets" / "advogado.jpg").convert("RGB")
    img.paste(ImageOps.fit(adv, (foto_lado, foto_lado), centering=(0.5, 0.18)), (m, y + 26))
    x = m + foto_lado + 24
    d.text((x, y + 26), NOME_CURTO, font=f_nome, fill=TINTA)
    d.text((x, y + 26 + int(f_nome.size * 1.3)), f"Advogado · {OAB} · Linhares/ES", font=f_sub, fill=(85, 85, 85))
    ass = Image.open(RAIZ / "assets" / "assinatura-bordo.png").convert("RGBA")
    ass = ass.resize((int(ass.width * assinatura_alt / ass.height), assinatura_alt), Image.LANCZOS)
    img.paste(ass, (l - m - ass.width, y + 10), ass)


def imagem(p, l, a, destino, instagram):
    from PIL import Image, ImageDraw, ImageOps
    img = Image.new("RGB", (l, a), PAPEL)
    d = ImageDraw.Draw(img)
    foto = Image.open(RAIZ / "assets" / "fotos" / "posts" / f"{p['slug']}.jpg").convert("RGB")
    area = AREAS[p["area"]]
    if instagram:
        m = 72
        d.line((m, 92, l - m, 92), fill=TINTA, width=3)
        d.text((m, 110), area, font=serifa(34, "Text Semibold"), fill=BORDO)
        serie = "Você sabia?"
        d.text((l - m - d.textlength(serie, font=serifa(34, "Text Semibold")), 110), serie, font=serifa(34, "Text Semibold"), fill=TINTA)
        y_rod = a - 175
        f_resp = condensada(36)
        resp = quebrar(d, f"{p['destaque']} {p['resumo']}", f_resp, l - 2 * m)
        alt_resp = len(resp) * int(f_resp.size * 1.32)
        y_resp = y_rod - 44 - alt_resp
        f_tit, linhas = titulo_que_cabe(d, p["titulo"], l - 2 * m, 330, [80, 74, 68, 62, 56, 52, 48])
        alt_tit = len(linhas) * int(f_tit.size * 1.08)
        y_tit = y_resp - 60 - alt_tit          # título e resposta presos ao rodapé
        alt_foto = max(360, y_tit - 40 - 172)  # a foto ocupa o espaço que sobra
        img.paste(ImageOps.fit(foto, (l - 2 * m, alt_foto)), (m, 172))
        y = escrever(d, m, y_tit, linhas, f_tit, TINTA, 1.08)
        y += 22
        d.rectangle((m, y, m + 120, y + 7), fill=BORDO)
        escrever(d, m, y + 30, resp, f_resp, (42, 42, 42), 1.32)
        rodape_imagem(img, d, m, y_rod, l, 96, serifa(42, "Subheading Semibold"), condensada(28), 118)
    else:
        lado_foto = 470
        img.paste(ImageOps.fit(foto, (lado_foto, a)), (l - lado_foto, 0))
        m = 56
        largura = l - lado_foto - 2 * m
        d.line((m, 52, l - lado_foto - m, 52), fill=TINTA, width=3)
        d.text((m, 66), area, font=serifa(26, "Text Semibold"), fill=BORDO)
        d.text((m + d.textlength(area, font=serifa(26, "Text Semibold")) + 14, 66), "· Você sabia?", font=serifa(26, "Text"), fill=CINZA)
        y_rod = a - 128
        f_dest = condensada(32, "SemiBold SemiCondensed")
        f_tit, linhas = titulo_que_cabe(d, p["titulo"], largura, y_rod - 118 - 110, [58, 54, 50, 46, 42, 38])
        y = escrever(d, m, 118, linhas, f_tit, TINTA, 1.08)
        y += 18
        d.rectangle((m, y, m + 90, y + 6), fill=BORDO)
        d.text((m, y + 22), p["destaque"], font=f_dest, fill=BORDO)
        rodape_imagem(img, d, m, y_rod, l - lado_foto, 76, serifa(32, "Subheading Semibold"), condensada(22), 92)
    img.save(destino, "JPEG", quality=86, optimize=True, progressive=True)


def pagina_expediente(posts):
    """Expediente da publicação: dados exigidos pelo Centro Brasileiro do ISSN (IBICT) para conceder o ISSN."""
    primeiro = min(p["data"] for p in posts)
    a, m, _ = primeiro.split("-")
    issn = f"<dt>ISSN</dt><dd>{ISSN}</dd>" if ISSN else ""
    corpo = f"""<section class="conteudo coluna expediente">
  <p class="linha-topo"><b>Expediente</b> Você sabia? Informativos {NOME}</p>
  <h1>Expediente</h1>
  <dl>
    <dt>Título</dt><dd>Você sabia? Informativos {NOME}</dd>{issn}
    <dt>Editor responsável</dt><dd>{ADVOGADO}, advogado, {OAB}</dd>
    <dt>Instituição</dt><dd>{NOME}, Escritório de Advocacia</dd>
    <dt>Endereço</dt><dd>{ENDERECO}, CEP 29901-554</dd>
    <dt>Contato</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a> · {TELEFONE}</dd>
    <dt>Suporte</dt><dd>On-line, em <a href="{BASE}">{BASE.removeprefix("https://").rstrip("/")}</a></dd>
    <dt>Periodicidade</dt><dd>Fluxo contínuo, com publicação de novas matérias em média a cada dois dias</dd>
    <dt>Início da publicação</dt><dd>{MESES[int(m) - 1]} de {a}, Vol. 1</dd>
    <dt>Designação numérica</dt><dd>Um volume por ano civil: Vol. 1 (2026), Vol. 2 (2027) e assim por diante</dd>
    <dt>Idioma</dt><dd>Português</dd>
    <dt>Assuntos</dt><dd>Direito de Família, Sucessões, Direito Trabalhista, Direito Civil, Direito do Consumidor e Direito Previdenciário</dd>
    <dt>Linha editorial</dt><dd>Textos informativos e em tese sobre direitos do dia a dia, com base legal conferida em fontes oficiais, de acordo com o Provimento 205/2021 do Conselho Federal da OAB. Não substituem a análise individual de cada situação.</dd>
  </dl>
</section>
"""
    return (cabeca(f"Expediente | Você sabia? Informativos {NOME}", "Expediente da publicação Você sabia? Informativos Ferreira Advogados.",
                   f"{BASE}expediente.html", "") + corpo + rodape("") + "</body>\n</html>\n")


def pagina_apresentacao(posts):
    corpo = f"""<section class="conteudo coluna expediente">
  <p class="linha-topo"><b>Apresentação</b> Você sabia? Informativos {NOME}</p>
  <h1>Apresentação</h1>
  <div class="texto">
    <p><b>Você sabia? Informativos {NOME}</b> é uma publicação on-line de divulgação jurídica, editada por {ADVOGADO}, advogado ({OAB}), em Linhares/ES.</p>
    <p>Cada matéria responde, de forma direta, uma dúvida comum sobre direitos do dia a dia, nas áreas de Direito de Família, Sucessões, Direito do Trabalho, Direito Civil, Direito do Consumidor e Direito Previdenciário.</p>
    <p>O público é o cidadão que não é da área jurídica. Por isso as matérias trazem a resposta logo no início, os pontos principais em poucas linhas, um exemplo do dia a dia e, para quem quiser se aprofundar, o texto completo, as perguntas frequentes e a base legal.</p>
    <p>Toda afirmação jurídica é conferida no texto oficial da lei, de súmulas ou de decisões de tribunais superiores. As matérias são informativas e em tese, de acordo com o Provimento 205/2021 do Conselho Federal da OAB, e não substituem a análise individual de cada situação.</p>
    <p>A publicação é contínua: novas matérias entram à medida que ficam prontas, organizadas em um volume por ano. Veja os <a href="volumes.html">volumes publicados</a> e o <a href="expediente.html">expediente</a>.</p>
  </div>
</section>
"""
    return (cabeca(f"Apresentação | Você sabia? Informativos {NOME}", "Apresentação da publicação Você sabia? Informativos Ferreira Advogados.",
                   f"{BASE}apresentacao.html", "") + corpo + rodape("") + "</body>\n</html>\n")


def pagina_volumes(posts):
    anos = sorted({p["data"][:4] for p in posts}, reverse=True)
    blocos = []
    for ano in anos:
        do_ano = [p for p in posts if p["data"][:4] == ano]
        itens = "".join(f'<li><a href="posts/{p["slug"]}.html">{e(p["titulo"])}</a><small>{AREAS[p["area"]]} · {data_curta(p["data"])}</small></li>' for p in do_ano)
        atual = " (volume atual)" if ano == anos[0] else ""
        blocos.append(f'<section class="volume"><h2>{volume(ano + "-01-01")}{atual}</h2><p>{len(do_ano)} matérias publicadas</p><ol>{itens}</ol></section>')
    corpo = f"""<section class="conteudo coluna expediente">
  <p class="linha-topo"><b>Volumes publicados</b> Você sabia? Informativos {NOME}</p>
  <h1>Volumes publicados</h1>
  <p class="chamada">Um volume por ano civil. As matérias entram no volume do ano em que são publicadas.</p>
  {"".join(blocos)}
</section>
"""
    return (cabeca(f"Volumes publicados | Você sabia? Informativos {NOME}", "Volumes publicados de Você sabia? Informativos Ferreira Advogados.",
                   f"{BASE}volumes.html", "") + corpo + rodape("") + "</body>\n</html>\n")


def pagina_serie(chave, posts):
    s = SERIES[chave]
    da_serie = sorted([p for p in posts if p.get("serie") == chave], key=lambda p: p["ordem"])
    cartoes = "\n".join("  " + cartao(p) for p in da_serie)
    corpo = f"""<section class="abertura"><div class="conteudo">
  <div>
    <p class="linha-topo"><b>Série</b> {len(da_serie)} informativos</p>
    <h1>{s["titulo"]}</h1>
    <p class="chamada">{s["descricao"]}</p>
    {assinatura("")}
  </div>
</div></section>
<section class="conteudo vitrine">
  <div class="lista">
{cartoes}
  </div>
</section>
"""
    return (cabeca(f"{s['titulo']} | Você sabia? Informativos {NOME}", s["descricao"], f"{BASE}{s['pagina']}", "")
            + corpo + rodape("") + "</body>\n</html>\n")


def main():
    posts = carregar()
    if not posts:
        sys.exit("Nenhum arquivo em conteudo/. Nada foi alterado.")
    (RAIZ / "posts").mkdir(exist_ok=True)
    (RAIZ / "imagens").mkdir(exist_ok=True)
    for p in posts:  # imagens antes das páginas: a versão da capa entra no og:image
        capa = RAIZ / "imagens" / f"{p['slug']}-capa.jpg"
        insta = RAIZ / "imagens" / f"{p['slug']}-instagram.jpg"
        if "--imagens" in sys.argv or not capa.exists() or not insta.exists():
            imagem(p, 1200, 630, capa, False)
            imagem(p, 1080, 1350, insta, True)
        (RAIZ / "posts" / f"{p['slug']}.html").write_text(pagina_post(p, posts), encoding="utf-8")
    (RAIZ / "index.html").write_text(pagina_inicial(posts), encoding="utf-8")
    (RAIZ / "artes.html").write_text(pagina_artes(posts), encoding="utf-8")
    (RAIZ / "expediente.html").write_text(pagina_expediente(posts), encoding="utf-8")
    (RAIZ / "apresentacao.html").write_text(pagina_apresentacao(posts), encoding="utf-8")
    (RAIZ / "volumes.html").write_text(pagina_volumes(posts), encoding="utf-8")
    for chave, s in SERIES.items():
        if any(p.get("serie") == chave for p in posts):
            (RAIZ / s["pagina"]).write_text(pagina_serie(chave, posts), encoding="utf-8")
    urls = [BASE] + [f"{BASE}{s['pagina']}" for s in SERIES.values()] + [f"{BASE}apresentacao.html", f"{BASE}volumes.html", f"{BASE}expediente.html"] + [f"{BASE}posts/{p['slug']}.html" for p in posts]
    linhas = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    (RAIZ / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{linhas}\n</urlset>\n',
        encoding="utf-8")
    (RAIZ / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
    nao = cabeca(f"Página não encontrada | {NOME}", "Página não encontrada.", BASE, "/") + """<section class="conteudo coluna nao-encontrada">
  <p class="linha-topo"><b>Erro 404</b> Página não encontrada</p>
  <h1>Este endereço não existe ou mudou de lugar.</h1>
  <p><a class="botao botao-linha" href="/index.html">Ver os informativos</a></p>
</section>
""" + rodape("/") + "</body>\n</html>\n"
    (RAIZ / "404.html").write_text(nao, encoding="utf-8")
    print(f"{len(posts)} posts gerados.")
    print("Mais recente:", f"{BASE}posts/{posts[0]['slug']}.html")


if __name__ == "__main__":
    main()
