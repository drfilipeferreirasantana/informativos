# Informativos "Você sabia?" da Ferreira Advogados

Site separado do site institucional, em HTML puro, publicado pelo GitHub Pages.
Não tem gerador nem etapa de construção: cada post é um arquivo HTML em `posts/`.

Endereço previsto: https://drfilipeferreirasantana.github.io/informativos/

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
   Em um ou dois minutos o endereço acima passa a funcionar.

## Como acrescentar um post

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

## Como ligar ao site principal

Basta um link no site institucional apontando para o endereço dos informativos. Opcionalmente, o endereço pode virar `informativos.escritorioferreiraadv.com.br`: crie um registro CNAME no DNS apontando para `drfilipeferreirasantana.github.io` e informe o domínio em **Settings > Pages > Custom domain**. Nesse caso, troque o endereço antigo nos arquivos (`canonical`, `og:url`, `sitemap.xml` e `robots.txt`).

Filipe Ferreira Santana · OAB/ES 37.159
