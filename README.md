# Informativos "Você sabia?" da Ferreira Advogados

Site separado do site institucional, em HTML puro, publicado pelo GitHub Pages.
Não tem gerador nem etapa de construção: cada post é um arquivo HTML em `posts/`.

Endereço: https://informativos.escritorioferreiraadv.com.br/ (o arquivo `CNAME` informa esse domínio ao GitHub Pages).
O site institucional (https://escritorioferreiraadv.com.br/, repositório `site-ferreira-advogados`) mostra uma faixa curta "Você sabia?" com o link para cá.

## Como publicar pela primeira vez

1. No GitHub, crie o repositório **informativos** (público) na conta `drfilipeferreirasantana`.
2. Nesta pasta, rode:

```bash
git remote add origin https://github.com/drfilipeferreirasantana/informativos.git
```

```bash
git push -u origin main
```

3. No GitHub, abra **Settings > Pages**, escolha **Deploy from a branch**, branch `main`, pasta `/ (root)` e salve.
   Em **Custom domain** deve aparecer `informativos.escritorioferreiraadv.com.br` (vem do arquivo `CNAME`).
4. No painel da Cloudflare, domínio `escritorioferreiraadv.com.br`, aba **DNS**, crie o registro:
   - Tipo `CNAME`, nome `informativos`, destino `drfilipeferreirasantana.github.io`, proxy **desligado** (nuvem cinza, "DNS only").
5. Volte em **Settings > Pages**, espere o certificado ficar pronto e marque **Enforce HTTPS**.

## Automação

A tarefa agendada **informativo-voce-sabia** (app Claude, seção "Agendadas") roda às 8h, a cada 2 dias: lê os Alertas do Google, pesquisa novidades na internet, confere a base legal na biblioteca do escritório, escreve o post, publica (commit e push) e manda por e-mail o link, uma legenda pronta para as redes e o link de compartilhamento no WhatsApp. Ela só roda com o app Claude aberto; se ele estiver fechado no horário, roda quando o app abrir.

## Como acrescentar um post à mão

1. Copie `modelo-post.html` para `posts/nome-do-post.html` (letras minúsculas, sem acento, palavras separadas por hífen).
2. Troque tudo o que está em MAIÚSCULAS e apague a linha `<meta name="robots" content="noindex">` e o comentário do topo.
3. No `index.html`, logo abaixo da linha `<!-- NOVOS POSTS ... -->`, cole o cartão:

```html
<a class="cartao" data-area="familia" href="posts/nome-do-post.html"><span class="meta">Direito de Família · 7 de novembro de 2026</span><h2>Você sabia que ...?</h2><p>Resumo curto.</p><span class="ler">Ler o informativo</span></a>
```

   Valores de `data-area`: `familia`, `sucessoes`, `trabalhista`, `consumidor`, `previdenciario`.
   Se usar uma área nova, acrescente o botão correspondente em `<div class="filtros">`.
4. Acrescente o endereço do post no `sitemap.xml`.
5. Faça o commit e o push. O GitHub Pages publica sozinho.

A página inicial mostra 12 cartões por vez, só com texto, e carrega o restante pelo botão "Ver mais informativos". Por isso ela continua leve mesmo com muitos posts.

## De onde vêm os temas

- **Alertas do Google** que chegam ao e-mail do escritório (pacto antenupcial, pensão alimentícia, divórcio e patrimônio, holding familiar, herança digital).
- **Pesquisa na internet** de dúvidas recorrentes nas áreas de atuação.

Regras para cada post:
- Texto próprio, sem copiar a notícia. A notícia aparece só como link em "Notícia de referência".
- Toda afirmação jurídica com base legal conferida no texto oficial (biblioteca do escritório ou site oficial).
- Caráter informativo, sem promessa de resultado, sem caso de cliente e sem chamada para contratar (Provimento 205/2021 do CFOAB e CED, arts. 39 a 47). As notas de pesquisa sobre essas regras estão no repositório `site-ferreira-advogados`, em `docs/research_notes`.

## Ligação com o site principal

A faixa "Você sabia?" da página inicial do site institucional aponta para https://informativos.escritorioferreiraadv.com.br/. Se o endereço mudar, troque-o nos arquivos (`canonical`, `og:url`, links de compartilhar, `sitemap.xml`, `robots.txt`, `CNAME`), na faixa do site institucional (`construir_site.py`) e na tarefa agendada.

Filipe Ferreira Santana · OAB/ES 37.159
