# Informativos "Você sabia?" da Ferreira Advogados

Site separado do site institucional, em HTML puro, publicado pelo GitHub Pages.
Cada post é um arquivo de conteúdo em `conteudo/`; o `ferramentas/gerar.py` monta as páginas no padrão definido em `docs/padrao-dos-posts.md` (estrutura, cores, imagens, contato pelo WhatsApp).

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

## Artes para as redes

Todas as artes ficam em https://informativos.escritorioferreiraadv.com.br/artes.html (página fora do Google): arte do Instagram, capa para WhatsApp e Facebook, e botão que envia o link já com a prévia.

## Automação

A tarefa agendada **informativo-voce-sabia** (app Claude, seção "Agendadas") roda às 8h, a cada 2 dias: lê os Alertas do Google, pesquisa novidades na internet, confere a base legal na biblioteca do escritório, escreve o post, publica (commit e push) e manda por e-mail o link, uma legenda pronta para as redes e o link de compartilhamento no WhatsApp. Ela só roda com o app Claude aberto; se ele estiver fechado no horário, roda quando o app abrir.

## Como acrescentar um post à mão

1. Copie um arquivo de `conteudo/` para `conteudo/AAAA-MM-DD-nome-do-post.json` e troque os campos (o formato está no topo de `ferramentas/gerar.py`).
2. Rode `python ferramentas/gerar.py`. Ele cria a página em `posts/`, a capa de compartilhamento e a arte do Instagram em `imagens/`, e refaz a página inicial e o `sitemap.xml`.
3. Faça o commit e o push. O GitHub Pages publica sozinho.

Áreas aceitas: `familia`, `sucessoes`, `trabalhista`, `civil`, `consumidor`, `previdenciario`. O gerador recusa texto com travessão.

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
