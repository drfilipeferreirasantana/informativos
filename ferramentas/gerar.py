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
# Título da publicação registrado no pedido de ISSN (IBICT): escrito sempre igual, sem sinais gráficos no meio.
# "Você sabia?" é o nome da seção de perguntas e respostas, não o título.
TITULO = "Informativos Ferreira Advogados"
COLUNA = "Você sabia?"
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
    "grandes-causas": {
        "titulo": "Grandes causas trabalhistas",
        "aba": "Grandes causas",
        "pagina": "grandes-causas.html",
        "descricao": "Informativos sobre as questões trabalhistas que costumam exigir mais prova e cálculos mais detalhados: contratação como PJ, gerentes e cargos de confiança, bancários, equiparação salarial, salário pago por fora, acidente e doença do trabalho, burnout, indenização à família e o valor do dano moral.",
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
    if not arq.exists():
        return "0"
    dados = arq.read_bytes()
    if arq.suffix in (".css", ".js", ".html", ".json"):
        dados = dados.replace(bytes([13, 10]), bytes([10]))  # mesmo hash no Windows e no GitHub
    return hashlib.md5(dados).hexdigest()[:8]


def hoje():
    """Data de hoje em Brasília (UTC-3), ou a data passada em --ate AAAA-MM-DD para ver uma prévia."""
    from datetime import datetime, timedelta, timezone
    for i, a in enumerate(sys.argv):
        if a == "--ate" and i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return datetime.now(timezone(timedelta(hours=-3))).date().isoformat()


def volume(iso):
    """Designação numérica exigida pelo ISSN: um volume por ano civil, a partir de 2026."""
    ano = int(iso[:4])
    return f"Vol. {ano - 2025} {ano}"


def pagina_do_volume(ano):
    """Endereço da página de cada volume (ex.: vol-1-2026.html)."""
    ano = int(ano)
    return f"vol-{ano - 2025}-{ano}.html"


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
<meta property="og:site_name" content="{TITULO}">
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
  <a class="marca" href="{base}index.html">
    <img src="{base}assets/emblema-escuro.png" width="26" height="26" alt=""><b>{TITULO}</b>
  </a>
  <nav aria-label="Principal">
    <a href="{base}index.html">Informativos</a>
    <a href="{SITE}">Site do escritório</a>
    <a class="nav-whats" href="{WHATS_GERAL}" target="_blank" rel="noopener">{ICONE_WHATS}<span>WhatsApp</span></a>
  </nav>
</div></header>
<nav class="barra-revista" aria-label="Publicação"><div class="conteudo">
  <a href="{base}apresentacao.html">Apresentação</a>
  <a href="{base}expediente.html">Expediente</a>
  <a href="{base}{pagina_do_volume(hoje()[:4])}">Volume atual: {volume(hoje())}</a>
  <a href="{base}volumes.html#anteriores">Volumes anteriores</a>
</div></nav>
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
      <h3>{TITULO}</h3>{issn}
      <p>Editor responsável: {ADVOGADO}, {OAB}</p>
      <p>{ENDERECO}</p>
      <p class="rodape-links"><a href="{base}apresentacao.html">Apresentação</a> · <a href="{base}volumes.html">Volumes publicados</a> · <a href="{base}expediente.html">Expediente</a></p>
    </div>
    <div>
      <h3>Contato</h3>
      <ul class="contatos">{itens}</ul>
    </div>
  </div>
  <p class="legal"><span class="direitos"><span class="copyright" aria-label="Copyright">©</span> {hoje()[:4]} {NOME}, Escritório de Advocacia. Todos os direitos reservados.</span>
  Conteúdo de caráter informativo, que não substitui a análise individual de cada situação.</p>
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
        "isPartOf": {"@type": "PublicationVolume", "volumeNumber": str(int(p["data"][:4]) - 2025),
                     "url": f"{BASE}{pagina_do_volume(p['data'][:4])}",
                     "isPartOf": {"@type": "Periodical", "name": TITULO, "url": BASE}},
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
  <p class="aviso">Publicado em <time datetime="{p['data']}">{data_extenso(p['data'])}</time>. Texto informativo. Cada situação depende de análise própria, com base nos documentos e nos fatos do caso.</p>
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
    return (cabeca(f"{p['titulo']} | {TITULO}", p["resumo"], url, "../", "article",
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
    <p class="linha-topo"><b>Informativos</b> <span class="marca-nome"><img src="assets/emblema-escuro.png" width="22" height="22" alt="">{NOME}</span> <a href="{pagina_do_volume(hoje()[:4])}">{volume(hoje())}</a></p>
    <h1>{COLUNA}</h1>
    <p class="chamada">Dúvidas comuns sobre família, herança, trabalho, compras e INSS, respondidas de forma direta</p>
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
    return (cabeca(TITULO,
                   "Dúvidas comuns sobre família, herança, trabalho, compras e INSS, respondidas por Filipe Ferreira, advogado em Linhares/ES.",
                   BASE, "") + corpo + rodape("") + SCRIPT_LISTA + "\n</body>\n</html>\n")


def sem_acento(t):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")


def codigo(p):
    return f"{p['numero']:03d}"


SCRIPT_ARTES = """<script>
(function () {
  var itens = [].slice.call(document.querySelectorAll('#painel .arte'));
  var campo = document.getElementById('busca'), contador = document.getElementById('contador');
  var area = '', situacao = '';
  function limpo(t) { return t.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').trim(); }
  function aplicar() {
    var q = limpo(campo.value).replace(/^n[ºo°]?\\s*(?=\\d)/, ''), n = 0;
    var g = /^g\\s*(\\d+)$/.exec(q), num = /^\\d+$/.test(q);
    itens.forEach(function (el) {
      var ok = (!area || el.dataset.area === area) && (!situacao || el.dataset.situacao === situacao);
      if (ok && q) {
        if (g) ok = el.dataset.google === String(parseInt(g[1], 10));
        else if (num) ok = el.dataset.numero === String(parseInt(q, 10));
        else ok = q.split(/\\s+/).every(function (w) { return el.dataset.busca.indexOf(w) > -1; });
      }
      el.hidden = !ok;
      if (ok) n++;
    });
    contador.textContent = n === 1 ? '1 arte' : n + ' artes';
  }
  function grupo(sel, definir) {
    var bs = [].slice.call(document.querySelectorAll(sel + ' button'));
    bs.forEach(function (b) {
      b.addEventListener('click', function () {
        bs.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        definir(b.dataset.valor); aplicar();
      });
    });
  }
  grupo('#f-area', function (v) { area = v; });
  grupo('#f-situacao', function (v) { situacao = v; });
  campo.addEventListener('input', aplicar);
  aplicar();
})();
</script>"""


SCRIPT_CONTADOR = """<script>
(function () {
  var URL_RESUMO = 'https://sistema.filipeferreiraadv.com/api/public/site/resumo';
  var caixa = document.getElementById('contador-site'), nota = document.getElementById('contador-nota');
  function campo(n) { return caixa.querySelector('[data-c="' + n + '"]'); }
  function num(v) { return typeof v === 'number' ? v.toLocaleString('pt-BR') : '...'; }
  function atualizar() {
    fetch(URL_RESUMO, { cache: 'no-store' }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    }).then(function (j) {
      var s = 'informativos';
      campo('online').textContent = num((j.online || {})[s]);
      campo('hoje').textContent = num(((j.hoje || {})[s] || {}).visitas);
      campo('mes').textContent = num(((j.mes || {})[s] || {}).visitas);
      campo('total').textContent = num(((j.total || {})[s] || {}).visitas);
      if (j.desde) { var d = j.desde.split('-'); campo('desde').textContent = 'visitas desde ' + d[2] + '/' + d[1] + '/' + d[0]; }
      caixa.classList.add('ativo');
      nota.textContent = 'Site de informativos. Cada entrada no site conta como uma visita (quem volta outro dia conta de novo). "Online agora" são as pessoas com uma página aberta nos últimos 2 minutos. Atualiza a cada 30 segundos; suas visitas a este painel não contam.';
    }).catch(function () {
      caixa.classList.remove('ativo');
      nota.textContent = 'O contador passa a mostrar os números assim que o sistema do escritório for atualizado.';
    });
  }
  atualizar();
  setInterval(function () { if (!document.hidden) atualizar(); }, 30000);
})();
</script>"""


def pagina_artes(posts, programados):
    """Página só para o Dr. Filipe (fora do Google): painel das artes, com busca pelo nº, tema ou área."""
    itens = []
    ordem = sorted(posts, key=lambda p: -p["numero"]) + sorted(programados, key=lambda p: p["numero"])
    for p in ordem:
        no_ar = p in posts
        cod = codigo(p)
        vi = versao('imagens/' + p['slug'] + '-instagram.jpg')
        vc = versao('imagens/' + p['slug'] + '-capa.jpg')
        url = f"{BASE}posts/{p['slug']}.html"
        compartilhar = f"https://wa.me/?text={quote(p['titulo'] + ' ' + url + '?v=' + str(p['numero']))}"
        google = p.get("google")
        busca = sem_acento(" ".join([p["titulo"], p["slug"].replace("-", " "), AREAS[p["area"]], p.get("destaque", "")]))
        situacao = (f"Publicado em {data_curta(p['data'])}" if no_ar
                    else f"Programado para {data_curta(p['data'])}")
        extra = f'<span class="selo-google">Google nº {google:02d}</span>' if google else ""
        if no_ar:
            acoes = f"""<a class="botao botao-whatsapp" href="{compartilhar}" target="_blank" rel="noopener">{ICONE_WHATS}Enviar no WhatsApp</a>
  <a class="botao botao-linha" href="posts/{p['slug']}.html">Abrir o post</a>"""
        else:
            acoes = '<p class="aviso-programado">O post e o link entram no ar nessa data.</p>'
        itens.append(f"""<div class="arte" data-numero="{p['numero']}" data-area="{p['area']}" data-situacao="{'publicado' if no_ar else 'programado'}" data-google="{google or ''}" data-busca="{e(busca)}">
  <img src="imagens/{p['slug']}-instagram.jpg?v={vi}" width="1080" height="1350" loading="lazy" alt="">
  <div><p class="ficha"><span class="codigo">Nº {cod}</span>{extra}</p>
  <b>{e(p['titulo'])}</b>
  <small class="{'' if no_ar else 'programado'}">{AREAS[p['area']]} · {situacao}</small>
  <a class="botao botao-linha" href="imagens/{p['slug']}-instagram.jpg?v={vi}" download="{cod}-{p['slug']}-instagram.jpg">Baixar arte do Instagram</a>
  <a class="botao botao-linha" href="imagens/{p['slug']}-capa.jpg?v={vc}" download="{cod}-{p['slug']}-capa.jpg">Baixar capa (WhatsApp e Facebook)</a>
  {acoes}</div>
</div>""")
    curto = {"familia": "Família", "sucessoes": "Sucessões", "trabalhista": "Trabalhista", "civil": "Civil",
             "consumidor": "Consumidor", "previdenciario": "Previdenciário"}
    usadas = [k for k in AREAS if any(p["area"] == k for p in ordem)]
    b_area = '<button type="button" data-valor="" aria-pressed="true">Todas as áreas</button>' + "".join(
        f'<button type="button" data-valor="{k}" aria-pressed="false">{curto.get(k, AREAS[k])}</button>' for k in usadas)
    b_sit = ('<button type="button" data-valor="" aria-pressed="true">Publicadas e programadas</button>'
             f'<button type="button" data-valor="publicado" aria-pressed="false">Publicadas ({len(posts)})</button>'
             f'<button type="button" data-valor="programado" aria-pressed="false">Programadas ({len(programados)})</button>')
    corpo = f"""<section class="artes conteudo">
  <h1>Painel das artes</h1>
  <p>Página de uso do escritório. Cada informativo tem um número (Nº), que também vai no nome do arquivo baixado. Busque pelo número, pelo tema ou por uma palavra. Para achar pela postagem do Google, digite G e o número (ex.: G12).</p>
  <div class="contador-site" id="contador-site" aria-live="polite">
    <div class="online"><b data-c="online">...</b><small><i></i>online agora</small></div>
    <div><b data-c="hoje">...</b><small>visitas hoje</small></div>
    <div><b data-c="mes">...</b><small>visitas no mês</small></div>
    <div><b data-c="total">...</b><small data-c="desde">visitas no total</small></div>
    <p id="contador-nota">Buscando os números no sistema do escritório...</p>
  </div>
  <div class="painel-busca">
    <label for="busca">Buscar arte</label>
    <input id="busca" type="search" placeholder="Ex.: 47, pensão, aviso prévio, G12" autocomplete="off">
    <span id="contador" aria-live="polite"></span>
  </div>
  <div class="filtros" id="f-area" role="group" aria-label="Filtrar por área">{b_area}</div>
  <div class="filtros" id="f-situacao" role="group" aria-label="Filtrar por situação">{b_sit}</div>
  <div class="lista" id="painel">{"".join(itens)}</div>
</section>
"""
    return (cabeca(f"Painel das artes | {NOME}", "Artes dos informativos para as redes.", f"{BASE}artes.html", "", robots=True)
            + corpo + rodape("") + SCRIPT_ARTES + SCRIPT_CONTADOR + "\n</body>\n</html>\n")


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
  <p class="linha-topo"><b>Expediente</b> {TITULO}</p>
  <h1>Expediente</h1>
  <dl>
    <dt>Título</dt><dd>{TITULO}</dd>{issn}
    <dt>Seção</dt><dd>{COLUNA} (perguntas e respostas sobre direitos do dia a dia)</dd>
    <dt>Corpo editorial</dt><dd>Editor responsável e autor das matérias: {ADVOGADO}, advogado, {OAB}</dd>
    <dt>Instituição responsável e editora</dt><dd>{NOME}, Escritório de Advocacia</dd>
    <dt>Endereço</dt><dd>{ENDERECO}, CEP 29901-554</dd>
    <dt>Contato</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a> · {TELEFONE}</dd>
    <dt>Suporte</dt><dd>On-line, em <a href="{BASE}">{BASE.removeprefix("https://").rstrip("/")}</a></dd>
    <dt>Periodicidade</dt><dd>Fluxo contínuo, com novas matérias publicadas ao longo de todo o ano</dd>
    <dt>Início da publicação</dt><dd>{MESES[int(m) - 1]} de {a}, {volume(primeiro)}</dd>
    <dt>Designação numérica</dt><dd>Um volume por ano civil: Vol. 1 2026, Vol. 2 2027, Vol. 3 2028 e assim por diante</dd>
    <dt>Volumes</dt><dd><a href="{pagina_do_volume(hoje()[:4])}">Volume atual: {volume(hoje())}</a> · <a href="volumes.html#anteriores">Volumes anteriores</a></dd>
    <dt>Idioma</dt><dd>Português</dd>
    <dt>Assuntos</dt><dd>Direito de Família, Sucessões, Direito Trabalhista, Direito Civil, Direito do Consumidor e Direito Previdenciário</dd>
    <dt>Linha editorial</dt><dd>Textos informativos e em tese sobre direitos do dia a dia, com base legal conferida em fontes oficiais, de acordo com o Provimento 205/2021 do Conselho Federal da OAB. Não substituem a análise individual de cada situação.</dd>
  </dl>
</section>
"""
    return (cabeca(f"Expediente | {TITULO}", f"Expediente da publicação {TITULO}.",
                   f"{BASE}expediente.html", "") + corpo + rodape("") + "</body>\n</html>\n")


def pagina_apresentacao(posts):
    corpo = f"""<section class="conteudo coluna expediente">
  <p class="linha-topo"><b>Apresentação</b> {TITULO}</p>
  <h1>Apresentação</h1>
  <div class="texto">
    <p><b>{TITULO}</b> é uma publicação on-line de divulgação jurídica, editada por {ADVOGADO}, advogado ({OAB}), em Linhares/ES.</p>
    <p>As matérias saem na seção <b>{COLUNA}</b>. Cada uma responde, de forma direta, uma dúvida comum sobre direitos do dia a dia, nas áreas de Direito de Família, Sucessões, Direito do Trabalho, Direito Civil, Direito do Consumidor e Direito Previdenciário.</p>
    <p>O público é o cidadão que não é da área jurídica. Por isso as matérias trazem a resposta logo no início, os pontos principais em poucas linhas, um exemplo do dia a dia e, para quem quiser se aprofundar, o texto completo, as perguntas frequentes e a base legal.</p>
    <p>Toda afirmação jurídica é conferida no texto oficial da lei, de súmulas ou de decisões de tribunais superiores. As matérias são informativas e em tese, de acordo com o Provimento 205/2021 do Conselho Federal da OAB, e não substituem a análise individual de cada situação.</p>
    <p>A publicação é contínua: novas matérias entram à medida que ficam prontas, organizadas em um volume por ano. Veja o <a href="{pagina_do_volume(hoje()[:4])}">volume atual ({volume(hoje())})</a>, os <a href="volumes.html#anteriores">volumes anteriores</a> e o <a href="expediente.html">expediente</a>.</p>
  </div>
</section>
"""
    return (cabeca(f"Apresentação | {TITULO}", f"Apresentação da publicação {TITULO}.",
                   f"{BASE}apresentacao.html", "") + corpo + rodape("") + "</body>\n</html>\n")


def lista_do_volume(do_ano):
    """Matérias do volume, da primeira à mais recente."""
    itens = "".join(f'<li><a href="posts/{p["slug"]}.html">{e(p["titulo"])}</a><small>{AREAS[p["area"]]} · {data_curta(p["data"])}</small></li>'
                    for p in sorted(do_ano, key=lambda p: p["numero"]))
    return f"<ol>{itens}</ol>"


def pagina_volume(ano, posts):
    do_ano = [p for p in posts if p["data"][:4] == ano]
    atual = ano == hoje()[:4]
    situacao = "Volume atual, em publicação contínua" if atual else "Volume encerrado"
    corpo = f"""<section class="conteudo coluna expediente">
  <p class="linha-topo"><b>{volume(ano + "-01-01")}</b> {TITULO}</p>
  <h1>{volume(ano + "-01-01")}</h1>
  <p class="chamada">{situacao}. {len(do_ano)} matérias publicadas em {ano}, na seção {COLUNA}.</p>
  <section class="volume">{lista_do_volume(do_ano)}</section>
  <p class="rodape-links"><a href="volumes.html">Todos os volumes</a> · <a href="volumes.html#anteriores">Volumes anteriores</a> · <a href="expediente.html">Expediente</a></p>
</section>
"""
    return (cabeca(f"{volume(ano + '-01-01')} | {TITULO}", f"{volume(ano + '-01-01')} da publicação {TITULO}: matérias publicadas em {ano}.",
                   f"{BASE}{pagina_do_volume(ano)}", "") + corpo + rodape("") + "</body>\n</html>\n")


def pagina_volumes(posts):
    anos = sorted({p["data"][:4] for p in posts}, reverse=True)
    atual, anteriores = anos[0], anos[1:]
    do_atual = [p for p in posts if p["data"][:4] == atual]
    if anteriores:
        lista_ant = "".join(f'<li><a href="{pagina_do_volume(a)}">{volume(a + "-01-01")}</a><small>{sum(1 for p in posts if p["data"][:4] == a)} matérias</small></li>' for a in anteriores)
        bloco_ant = f"<ol>{lista_ant}</ol>"
    else:
        bloco_ant = f"<p>{volume(atual + '-01-01')} é o primeiro volume. Os volumes encerrados aparecem aqui a partir de {int(atual) + 1}.</p>"
    corpo = f"""<section class="conteudo coluna expediente">
  <p class="linha-topo"><b>Volumes</b> {TITULO}</p>
  <h1>Volumes</h1>
  <p class="chamada">Publicação em fluxo contínuo, com um volume por ano civil. As matérias entram no volume do ano em que são publicadas.</p>
  <section class="volume" id="atual"><h2>Volume atual: <a href="{pagina_do_volume(atual)}">{volume(atual + "-01-01")}</a></h2><p>{len(do_atual)} matérias publicadas</p>{lista_do_volume(do_atual)}</section>
  <section class="volume" id="anteriores"><h2>Volumes anteriores</h2>{bloco_ant}</section>
</section>
"""
    return (cabeca(f"Volumes | {TITULO}", f"Volume atual e volumes anteriores da publicação {TITULO}.",
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
    return (cabeca(f"{s['titulo']} | {TITULO}", s["descricao"], f"{BASE}{s['pagina']}", "")
            + corpo + rodape("") + "</body>\n</html>\n")


def main():
    todos = carregar()
    if not todos:
        sys.exit("Nenhum arquivo em conteudo/. Nada foi alterado.")
    # Publicação programada: o post só entra no site a partir da sua data ("data" no JSON).
    # O GitHub roda este gerador todo dia de manhã (.github/workflows/publicar-programados.yml).
    dia = hoje()
    posts = [p for p in todos if p["data"] <= dia]
    programados = [p for p in todos if p["data"] > dia]
    if not posts:
        sys.exit("Nenhum post com data até hoje. Nada foi alterado.")
    (RAIZ / "posts").mkdir(exist_ok=True)
    (RAIZ / "imagens").mkdir(exist_ok=True)
    tem_fontes = Path(FONTES_WIN + "SitkaVF.ttf").exists()
    for p in todos:  # artes de todos, inclusive os programados (no GitHub as artes já vêm prontas)
        capa = RAIZ / "imagens" / f"{p['slug']}-capa.jpg"
        insta = RAIZ / "imagens" / f"{p['slug']}-instagram.jpg"
        if "--imagens" in sys.argv or not capa.exists() or not insta.exists():
            if not tem_fontes:
                print(f"Aviso: sem as fontes para gerar as artes de {p['slug']}; gere no computador do escritório.")
                continue
            imagem(p, 1200, 630, capa, False)
            imagem(p, 1080, 1350, insta, True)
    for p in programados:  # página de post programado não fica no ar antes da data
        (RAIZ / "posts" / f"{p['slug']}.html").unlink(missing_ok=True)
    for p in posts:
        (RAIZ / "posts" / f"{p['slug']}.html").write_text(pagina_post(p, posts), encoding="utf-8")
    (RAIZ / "index.html").write_text(pagina_inicial(posts), encoding="utf-8")
    (RAIZ / "artes.html").write_text(pagina_artes(posts, programados), encoding="utf-8")
    (RAIZ / "expediente.html").write_text(pagina_expediente(posts), encoding="utf-8")
    (RAIZ / "apresentacao.html").write_text(pagina_apresentacao(posts), encoding="utf-8")
    (RAIZ / "volumes.html").write_text(pagina_volumes(posts), encoding="utf-8")
    anos = sorted({p["data"][:4] for p in posts})
    for ano in anos:
        (RAIZ / pagina_do_volume(ano)).write_text(pagina_volume(ano, posts), encoding="utf-8")
    series_no_ar = []
    for chave, s in SERIES.items():
        if any(p.get("serie") == chave for p in posts):
            (RAIZ / s["pagina"]).write_text(pagina_serie(chave, posts), encoding="utf-8")
            series_no_ar.append(s)
        else:
            # série só com programados: a página só entra no ar com o primeiro post publicado
            (RAIZ / s["pagina"]).unlink(missing_ok=True)
    urls = [BASE] + [f"{BASE}{s['pagina']}" for s in series_no_ar] +[f"{BASE}apresentacao.html", f"{BASE}volumes.html", f"{BASE}expediente.html"] + [f"{BASE}{pagina_do_volume(a)}" for a in anos] + [f"{BASE}posts/{p['slug']}.html" for p in posts]
    linhas = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    (RAIZ / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{linhas}\n</urlset>\n',
        encoding="utf-8")
    (RAIZ / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
    nao = cabeca(f"Página não encontrada | {TITULO}", "Página não encontrada.", BASE, "/") + """<section class="conteudo coluna nao-encontrada">
  <p class="linha-topo"><b>Erro 404</b> Página não encontrada</p>
  <h1>Este endereço não existe ou mudou de lugar.</h1>
  <p><a class="botao botao-linha" href="/index.html">Ver os informativos</a></p>
</section>
""" + rodape("/") + "</body>\n</html>\n"
    (RAIZ / "404.html").write_text(nao, encoding="utf-8")
    print(f"{len(posts)} posts publicados até {dia}.")
    if programados:
        print(f"{len(programados)} programados; o próximo entra em {min(p['data'] for p in programados)}.")
    print("Mais recente:", f"{BASE}posts/{posts[0]['slug']}.html")


if __name__ == "__main__":
    main()
