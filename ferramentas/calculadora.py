"""Página da Calculadora de rescisão (pedido do Dr. Filipe, 14/11/2026).

Fica fixada no topo da aba "Direito Trabalhista" da página inicial e é indicada
nos informativos sobre rescisão. O cálculo roda no navegador (assets/calculadora.js).
Pensada para a busca do Google: resposta direta no início, explicação de cada verba,
perguntas frequentes e dados estruturados (WebApplication, FAQPage e autor advogado).
"""
import json

PAGINA = "calculadora-rescisao.html"
TITULO_PAG = "Calculadora de rescisão trabalhista"
DESCRICAO = ("Calcule as verbas rescisórias: saldo de salário, aviso prévio proporcional, 13º, férias com 1/3 "
             "e multa do FGTS, na dispensa sem justa causa, pedido de demissão, acordo ou justa causa.")
# informativos que recebem o quadro "Calcule a sua rescisão"
PALAVRAS_POSTS = ("rescis", "aviso-previo", "fgts", "justa-causa", "demiss", "verbas", "multa-do-artigo",
                  "acordo-o-que-recebe", "termo-de-rescisao", "pedi-demissao", "salario-atrasado")

VERBAS = [
    ("Saldo de salário", "Os dias trabalhados no mês da saída, pagos em qualquer tipo de rescisão."),
    ("Aviso prévio", "30 dias, mais 3 dias por ano completo de empresa, até 90 dias (Lei 12.506/2011). Quando indenizado, o período conta como tempo de serviço e aumenta o 13º e as férias."),
    ("13º salário proporcional", "1/12 do salário por mês do ano com 15 dias ou mais de trabalho. Não é devido na justa causa."),
    ("Férias vencidas e proporcionais", "Sempre com o adicional de 1/3. As vencidas são pagas em qualquer rescisão; as proporcionais não são devidas na justa causa (Súmula 171 do TST) e são devidas no pedido de demissão (Súmula 261 do TST)."),
    ("Multa do FGTS", "40% do saldo do FGTS na dispensa sem justa causa; 20% na demissão por acordo; nada no pedido de demissão e na justa causa."),
]

FAQ = [
    ("O que são verbas rescisórias?", "São os valores que a empresa deve pagar ao empregado com carteira assinada quando o contrato de trabalho termina, como saldo de salário, aviso prévio, 13º proporcional, férias com 1/3 e, conforme o tipo de saída, a multa do FGTS."),
    ("Qual o prazo para a empresa pagar a rescisão?", "10 dias, contados do fim do contrato. Se atrasar, a empresa deve pagar multa no valor de um salário ao empregado (CLT, art. 477, §§ 6º e 8º)."),
    ("Quem pede demissão recebe o quê?", "Saldo de salário, 13º proporcional e férias vencidas e proporcionais com 1/3. Não há saque do FGTS, multa de 40% nem seguro-desemprego, e o aviso não cumprido pode ser descontado (CLT, art. 487, § 2º)."),
    ("Como funciona a demissão por acordo?", "O empregado recebe metade do aviso prévio indenizado e multa de 20% do FGTS, as demais verbas por inteiro, e pode sacar até 80% do FGTS, sem seguro-desemprego (CLT, art. 484-A)."),
    ("O valor da calculadora é o que vou receber?", "É uma estimativa bruta, antes de INSS e Imposto de Renda. Horas extras, comissões, adicionais, médias variáveis e o saldo real do FGTS mudam o resultado."),
]


def pagina(cabeca, rodape, base_url, assinatura, versao, e, oab, advogado, nome, site):
    url = f"{base_url}{PAGINA}"
    verbas = "".join(f"<li><b>{e(n)}:</b> {e(t)}</li>" for n, t in VERBAS)
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(r)}</p></details>" for q, r in FAQ)
    ld = json.dumps([
        {"@context": "https://schema.org", "@type": "WebApplication", "name": TITULO_PAG, "url": url,
         "applicationCategory": "FinanceApplication", "operatingSystem": "Navegador", "inLanguage": "pt-BR",
         "description": DESCRICAO, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "BRL"},
         "author": {"@type": "Person", "name": advogado, "jobTitle": f"Advogado, {oab}", "url": site},
         "publisher": {"@type": "LegalService", "name": nome, "url": site}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in FAQ]},
    ], ensure_ascii=False)
    corpo = f"""<article class="post calculadora">
<div class="conteudo coluna">
  <p class="linha-topo"><b>Direito Trabalhista</b> Ferramenta gratuita<a href="index.html">Todos os informativos</a></p>
  <h1>{TITULO_PAG}</h1>
  <div class="resposta"><strong>Verbas rescisórias</strong> são os valores que a empresa deve pagar ao empregado com carteira assinada quando o contrato termina. Informe os dados abaixo para estimar quanto você tem a receber.</div>
  <form id="calc" class="calc-form" novalidate>
    <label>Salário mensal (R$)<input name="salario" inputmode="decimal" placeholder="ex.: 2.500,00" required></label>
    <div class="calc-duas">
      <label>Data de entrada<input name="admissao" type="date" required></label>
      <label>Último dia de trabalho<input name="saida" type="date" required></label>
    </div>
    <label>Como o contrato terminou
      <select name="tipo">
        <option value="sem_justa">Fui dispensado sem justa causa</option>
        <option value="pedido">Pedi demissão</option>
        <option value="acordo">Demissão por acordo (art. 484-A)</option>
        <option value="justa">Fui dispensado por justa causa</option>
        <option value="experiencia">Fim do contrato de experiência</option>
        <option value="experiencia_antecipada">Dispensado antes do fim da experiência</option>
      </select></label>
    <label id="linha-aviso">Aviso prévio
      <select name="aviso"><option value="trabalhado">Trabalhado</option><option value="indenizado" selected>Indenizado (pago sem trabalhar)</option></select></label>
    <div class="calc-duas">
      <label>Férias vencidas não tiradas
        <select name="vencidas"><option value="0">Nenhuma</option><option value="1">1 período</option><option value="2">2 períodos</option></select></label>
      <label>Saldo do FGTS (opcional)<input name="fgts" inputmode="decimal" placeholder="se souber, do extrato"></label>
    </div>
    <button class="botao" type="submit">Calcular minha rescisão</button>
  </form>
  <section id="resultado" class="calc-resultado" hidden aria-live="polite"></section>
  <details class="entenda" open><summary>Como cada verba é calculada</summary>
  <div class="texto"><ul>{verbas}</ul>
  <p>O cálculo considera o salário informado. Quem recebe comissões, horas extras ou adicionais deve usar a média dessas parcelas, o que normalmente aumenta o valor.</p></div></details>
  <section class="faq"><h2>Perguntas frequentes</h2>{faq}</section>
  <div class="caixa"><b>Base legal</b><ul><li>CLT, arts. 146, 147, 477, 479, 484-A e 487</li><li>Lei 4.090/1962 (13º salário)</li><li>Lei 12.506/2011 (aviso prévio proporcional)</li><li>Lei 8.036/1990, art. 18 (multa do FGTS)</li><li>Súmulas 171 e 261 do TST</li></ul></div>
  <p class="aviso">Ferramenta informativa, revisada por {e(advogado)}, advogado ({oab}). O resultado é uma estimativa e não substitui a análise do caso com os documentos.</p>
  {assinatura}
</div>
</article>
"""
    extra = f'\n<script type="application/ld+json">{ld}</script>'
    return (cabeca(f"{TITULO_PAG} | Verbas rescisórias", DESCRICAO, url, "", "website", f"{base_url}assets/calculadora-capa.jpg", extra)
            + corpo + rodape("") + f'<script src="assets/calculadora.js?v={versao("assets/calculadora.js")}" defer></script>\n</body>\n</html>\n')


def cartao_fixo(e):
    return ('<a class="cartao fixado" data-area="trabalhista" data-fixo="1" href="calculadora-rescisao.html">'
            '<img src="assets/calculadora-p.jpg" width="480" height="300" loading="lazy" alt="">'
            '<span class="meta">Direito Trabalhista · Ferramenta</span>'
            f'<h2>{e(TITULO_PAG)}</h2>'
            '<span class="resposta-curta">Calcule suas verbas rescisórias.</span></a>')


def quadro_post(slug):
    if not any(k in slug for k in PALAVRAS_POSTS):
        return ""
    return ('<div class="caixa calc-chamada"><b>Calculadora de rescisão</b>'
            '<p>Estime saldo de salário, aviso prévio, 13º, férias e multa do FGTS.</p>'
            '<a class="botao botao-linha" href="../calculadora-rescisao.html">Calcular minha rescisão</a></div>')
