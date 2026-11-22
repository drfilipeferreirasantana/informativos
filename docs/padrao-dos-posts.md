# Padrão dos posts "Você sabia?"

Pesquisa feita em 8/11/2026 para definir que tipo de post atrai a atenção de possíveis clientes, como montar a estrutura e que cores, imagens, chamadas e funções cada post deve ter. Os geradores (`ferramentas/gerar.py`) e a tarefa automática seguem este documento.

Força da evidência: a maior parte do que existe sobre marketing jurídico vem de agências e fornecedores, sem amostra declarada. Onde o número for de fornecedor, isso está dito. As regras da OAB vêm das notas já conferidas no repositório `site-ferreira-advogados` (`docs/research_notes/.../regras_oab.md`).

## 1. Que tipo de post atrai possíveis clientes

- **Uma dúvida real por post, respondida logo no início.** As fontes convergem: o leitor chega com uma pergunta e procura a resposta, não uma apresentação do escritório. Escrever sobre o problema do leitor, sem jargão ([Sociosquares](https://www.sociosquares.com/blog/how-to-write-blog-posts-for-your-law-firm-that-actually-bring-in-clients/); [Lexicon Legal Content](https://www.lexiconlegalcontent.com/10-tips-to-help-legal-blog-writers-turn-readers-into-clients/)).
- **Título com as palavras que a pessoa digitaria no Google.** "Você sabia que...?" funciona como gancho, desde que o resto do título traga o termo de busca (pensão, divórcio, FGTS, herança) ([Hennessey](https://hennessey.com/blog/legal-blog-ideas-content-that-helps-law-firms-rank-and-convert/)).
- **Texto escaneável:** subtítulos claros, listas e parágrafos curtos, porque a leitura é no celular ([Forward Push](https://forwardpush.com/blog/how-to-structure-your-law-blog-to-attract-and-retain-clients/)).
- **Perguntas frequentes no fim** para responder as dúvidas seguintes do leitor e mantê-lo na página ([Edwards Legal Marketing](https://edwardslegalmarketing.com/law-firm-content-writing-that-converts-how-to-turn-educational-blogs-into-signed-cases/)).
- **Temas de Família que mais geram dúvida:** pensão (cálculo, revisão, atraso), guarda e convivência, divórcio com e sem filhos, partilha e regime de bens, inventário ([Advbox](https://advbox.com.br/blog/instagram-na-advocacia/); [TJPB](https://www.tjpb.jus.br/w/saiba-como-e-quando-solicitar-guarda-regulamenta%C3%A7%C3%A3o-de-visitas-e-pens%C3%A3o-aliment%C3%ADcia%C2%A0-1)).

## 2. Visual sem marcas de IA (decidido pelo Dr. Filipe em 8/11/2026)

O primeiro visual (marinho com dourado, Montserrat em negrito, selos arredondados, degradês, ícones em círculos, "Você sabia que..." em todo título, sempre 3 pontos e "Imagine:") é o padrão que ferramentas de IA produzem e que o público mais informado reconhece. Foi trocado por:

- **Formato de jornal (proposta A):** linha fina no topo com o número em bordô e a área; foto com borda reta, sem degradê; título; traço bordô curto; resposta; rodapé separado por linha com a foto pequena, o nome, a OAB e o emblema da estrela (desde 13/11/2026 a rubrica verdadeira não aparece no site nem nas artes).
- **Letras (proposta C):** título com serifa (Sitka Display nas artes; Source Serif 4 no site) e texto de apoio em condensada (Bahnschrift nas artes; Barlow Semi Condensed no site). Sitka e Bahnschrift são do Windows e não podem ir para a web, por isso o site usa as equivalentes livres do Google Fonts.
- **Cores:** papel claro (#ece7de), tinta quase preta (#161616) e **bordô** (#7a2333), a cor da gravata da foto oficial, só nos detalhes. Verde só no botão do WhatsApp. Nada de sombras fortes ou cantos arredondados.
- **Assinatura:** extraída da foto enviada pelo Dr. Filipe, em bordô e com 260 px de largura de propósito (marca visual, sem resolução para virar cópia em papel). Na página principal fica centralizada abaixo de "Advogado · OAB/ES 37.159", sem repetir a foto. Proteções (pedido de 8/11/2026): no site ela é fundo desenhado e não imagem, então não aparece "salvar imagem", não se arrasta e não reage a toque longo; o próprio arquivo tem linhas diagonais transparentes que picotam o traço quando ampliado. Nenhuma página consegue impedir um print de tela; por isso a defesa principal é a cópia sair inútil (baixa resolução, bordô e picotada).
- **Texto:** título como a pergunta direta que a pessoa faria ("A pensão acaba quando o filho faz 18 anos?"); "Você sabia?" é só o nome da série. A resposta curta é uma frase normal ("Não automaticamente."), não um selo em maiúsculas. De 2 a 4 pontos, conforme o tema. O exemplo do dia a dia não começa com "Imagine:".
- **Próximos passos para ficar 100%:** fotos reais do Dr. Filipe e do escritório no lugar de parte das fotos do Pexels; variar os formatos (pergunta, mito ou verdade, prazo, "o que fazer quando").

## 3. Estrutura do post

1. Linha de topo (número, área) e foto da área.
2. Título em pergunta direta.
3. Resposta curta em bordô, seguida da explicação em 1 ou 2 frases.
4. De 2 a 4 pontos numerados.
5. Situação do dia a dia (fictícia, marcada como ilustrativa).
6. "Entenda melhor" com o texto completo, recolhido.
7. Perguntas frequentes, base legal e notícia de referência.
8. Quem escreve: foto, nome, OAB, formação, IBDFAM, áreas, emblema da estrela e o botão "Conversar pelo WhatsApp".
9. Leia também: 3 informativos relacionados.

## 4. Imagens

**Regra de execução (8/11/2026): nenhuma foto se repete.** Cada informativo tem a sua foto, ligada ao tema do post (ex.: contas e calculadora para nome negativado, caixa de pertences para pedido de demissão, mão com aliança assinando para divórcio em cartório). As fotos vêm do Pexels (licença gratuita para uso comercial, sem atribuição obrigatória; origem registrada no campo `foto` de cada post) e ficam em `assets/fotos/posts/`. O gerador recusa post sem foto própria ou com foto igual à de outro post. Evitar fotos com texto em inglês legível e pessoas que já apareceram em outro post.


- **Foto real do advogado** perto do contato. Fornecedores relatam alta de 35% a 45% na conversão com fotos reais em vez de banco de imagens, em testes fora do setor jurídico. É indício, não prova ([AttorneySync](https://attorneysync.com/blog/photographs-real-lawyers-stock-images); [Custom Legal Marketing](https://custom.legal/practice-areas/personal-injury-law-firm-marketing/stock-photos-vs-ai-photos-vs-real-attorney-photos/)). A OAB permite foto, nome, OAB, formação e instituições (CED, art. 44, § 1º), e o TED-SP admitiu coluna com nome e foto do autor (16/10/2025).
- **Sem foto de banco** (martelo, balança genérica, casal brigando) e sem imagem de clientes.
- **Capa para compartilhar (1200 x 630, abaixo de 300 KB):** é a imagem que aparece quando o link é enviado no WhatsApp e no Facebook. O WhatsApp corta perto do quadrado, então o texto fica centralizado ([Screenhance](https://screenhance.com/blog/og-image-size-guide); [Andrew Baker](https://andrewbaker.ninja/2026/03/05/fix-thumbnail-previews-on-whatsapp-linkedin-x-guide/)).
- **Arte para o Instagram (1080 x 1350, formato 4:5):** foto da área, a pergunta em letras grandes, o destaque em dourado e o rodapé com a foto do Dr. Filipe e o emblema da estrela. Todas as artes ficam na página `artes.html` (fora do Google), com botões para baixar e enviar no WhatsApp. Carrosséis educativos são os que mais recebem "salvar", segundo dados de fornecedores ([Socialinsider](https://socialinsider.io/blog/instagram-carousel-research)). Uma arte única já serve; carrossel de 3 a 7 telas é o próximo passo ([ACE Conteúdo](https://aceconteudodigital.com.br/como-criar-conteudo-juridico-instagram/)).

## 5. Chamada para o WhatsApp (CTA)

- **Onde:** no bloco "Quem escreve" ao fim do post e na barra fixa do celular. Botão flutuante não pode cobrir o conteúdo e precisa ser testado no celular ([Chatsac](https://chatsac.com/blog/botao-whatsapp-site/)).
- **Mensagem pronta** com o tema do post ("Li o informativo ..."), para a conversa começar com contexto ([Wati](https://www.wati.io/pt-br/blog/botao-do-whatsapp-como-adicionar-o-widget-do-whatsapp-ao-site/)).
- **Texto do botão:** "Conversar pelo WhatsApp". O WhatsApp é dado de contato permitido (Provimento 205/2021, art. 4º, § 3º), e informar as áreas de atuação também é permitido (CED, art. 44, § 1º).
- **Limite da OAB:** a Cartilha do CFOAB (2024) veda chamada à contratação. Ficam de fora "contrate", "garanta seu direito", "fale agora com um advogado" e "análise gratuita do seu caso". A frase "Para tirar dúvidas sobre este assunto ou agendar um atendimento, o contato é pelo WhatsApp" foi pedida pelo Dr. Filipe e está na faixa de risco **médio** das notas do escritório. Se quiser risco baixo, troque por "Contato do escritório pelo WhatsApp".

## 6. Prévia no WhatsApp

- A prévia (imagem, título e descrição) só aparece se o WhatsApp conseguir ler a página. Um link enviado antes do HTTPS ficar pronto saiu sem prévia, e o WhatsApp guarda essa leitura falha por um tempo.
- Para forçar uma leitura nova, acrescente `?v=2` ao fim do endereço. Os botões "Enviar no WhatsApp" da página de artes já fazem isso.

## 7. Outras funções

- **Tempo de leitura** e data visíveis.
- **Autor com credenciais** no post e nos dados estruturados (Article com autor Person). É o sinal de confiança mais recomendado para conteúdo jurídico, que o Google trata como YMYL ([Rankings.io](https://rankings.io/blog/eeat-ymyl-for-lawyers/)).
- **Leia também** com 3 links internos, para o leitor seguir no site.
- **Compartilhar no WhatsApp** com título e link.
- **Leveza:** a página inicial só tem texto; imagens grandes só na capa de compartilhamento, que o leitor não baixa ao abrir o site.
- **Para depois:** medir cliques no WhatsApp por post (hoje o site de informativos não mede nada e não usa cookies; medir exige atualizar uma política de privacidade).

## 8. Para o Google indicar (decidido pelo Dr. Filipe em 14/11/2026)

O gerador já coloca em todo post, sem trabalho manual: dados da matéria (Article com autor, área e data de atualização), perguntas frequentes (FAQPage), trilha Informativos › área › matéria (BreadcrumbList), link para a página do autor (autor.html) e data de cada página no sitemap. O site está cadastrado no Google Search Console (arquivo google87e4dbb8c52dae81.html na raiz: nunca apagar).

Regra para cada post novo:
1. **Título = a pergunta que a pessoa digita no Google**, com as palavras dela ("Quem pede demissão tem direito a quê?").
2. **Resposta na primeira frase** (campos `destaque` e `resumo`): é o trecho que o Google e as respostas de IA copiam.
3. **FAQ com 3 a 5 perguntas reais**, de preferência as que chegam pela Iadã no WhatsApp. Cada resposta completa sozinha, em 1 a 3 frases.
4. **Subtítulos no `corpo` em forma de pergunta ou tema** (`<h2>`), e um link para outro informativo do mesmo assunto quando houver.
5. **Ao revisar um post já publicado** (lei nova, súmula nova, valor atualizado), preencher `"atualizado": "AAAA-MM-DD"` no JSON: a data aparece no post e avisa o Google.
6. **Temas muito buscados ganham ferramenta**, como a Calculadora de rescisão.
7. **Cada tema grande tem um guia completo (página-pilar)** em `ferramentas/pilares.py`: texto do começo ao fim do assunto, com links para os informativos do tema. Já no ar: Divórcio (`divorcio.html`) e Pensão alimentícia (`pensao-alimenticia.html`), aprovados em 14/11/2026, e Guarda dos filhos (`guarda-dos-filhos.html`), aprovado em 15/11/2026. Quando um post está em dois guias, o link do topo vai para o mais específico. Post novo do tema entra pelo slug na seção certa do guia; programado só aparece no guia quando for ao ar. Ao mudar o texto do guia, atualizar o campo `atualizado`.
8. **Pesquisa do site** (caixa na página inicial, `assets/busca.js`): lê o `busca.json` que o gerador cria com os guias, a calculadora e os posts publicados. Palavra nova que o cliente usa e não acha nada: incluir em `SINONIMOS` no `busca.js`.

## 9. Linguagem e voz do escritório (decidido pelo Dr. Filipe em 15/11/2026)

**Frase-assinatura da marca (escolhida pelo Dr. Filipe em 18/11/2026): "Seu direito importa. Nós o defendemos."** Vai no fim de todo carrossel, vídeo, post e no rodapé dos sites, sempre igual, para ser lembrada (estratégia de repetição). Sentimento que ela deve passar: força ao lado do cliente.

Frase que guia tudo: **"Conhecer o próprio direito é a primeira forma de protegê-lo."** O leitor deve terminar o informativo com **confiança no escritório**: sentir que encontrou quem domina o assunto.

**Tom: conselheiro firme e direto.** Diz o que precisa ser dito, sem rodeio e sem promessa de resultado.

1. **Sem linguagem de lei no texto corrido.** A regra vem traduzida para a vida real; o termo técnico só aparece entre parênteses ou na base legal. Ex.: em vez de "dano extrapatrimonial que ofenda a esfera moral ou existencial", escrever "ser humilhado, xingado ou exposto na frente dos colegas". Evitar também "a qualquer tempo" (usar "sem prazo"), "presumida" (explicar o efeito), "averiguação", "ensejar", "outrossim".
2. **Destaque com resposta completa**, nunca só "Pode gerar." ou "Depende.". Dizer quando sim e quando não, em até 40 caracteres (limite da arte): "Sim, se repetida ou em público."
3. **Sem a palavra "comum" para valorizar o tema** ("Dúvidas comuns", "Situações comuns"). Usar "o que mais acontece", "o erro mais frequente", "na prática".
4. **Texto impessoal**, sem "eu" nem "nós", e sem analogias de negócios. A experiência aparece pelo conteúdo: o erro que as pessoas cometem antes de procurar advogado, o que decide o caso, o que fazer primeiro.
5. **Exemplo inventado e típico** (campo `exemplo`), nunca ligado a cliente real.
6. **Alerta de erro na seção "Na prática"**: os erros que o escritório mais vê são sair de casa sem orientação, não guardar provas (apagar mensagens, não juntar documentos) e deixar o tempo passar.
7. **Fecho variado e com próximo passo.** "Cada caso depende de análise própria" pode aparecer, mas não igual em todos: junto, dizer o que levar à primeira conversa ou o que fazer agora.
8. **Verdade dos fatos primeiro**: quando couber, lembrar que o caso se constrói com tudo contado, inclusive o que pesa contra.
9. **Acordo primeiro, se for justo**: em Família e Consumidor, mostrar que dá para resolver sem processo quando o acordo protege a pessoa.

O que mais chega ao escritório, para escolher temas e exemplos:
- **Família:** medo de perder bens ou a empresa, de ficar longe dos filhos e de não saber por onde começar.
- **Trabalho:** todos os temas (rescisão e verbas, horas extras e jornada, assédio e dano moral, insalubridade e acidente). Pano de fundo: empregador que trata o trabalhador como instrumento e ignora a dignidade da pessoa.
- **Previdenciário:** benefício negado sem explicação, pedido feito sozinho e com erro, doente que não consegue trabalhar, dúvida sobre quando aposenta.
- **Consumidor e Cível:** empresa que não cumpre o contrato e deixa de lado a boa-fé.

## Publicação programada

- O campo `data` do JSON é o dia em que o post entra no site. Post com data futura fica guardado: não aparece na página inicial, nas séries, no sitemap nem tem página no ar.
- Todo dia às 6h05 (Brasília) o GitHub roda `ferramentas/gerar.py` (arquivo `.github/workflows/publicar-programados.yml`) e publica os posts do dia. Para publicar na hora, use o botão "Run workflow" na aba Actions do repositório.
- As artes (Instagram e capa) dos programados são geradas no computador do escritório, porque usam as fontes do Windows. Rode `python ferramentas/gerar.py` antes de enviar posts novos.
- Prévia de como o site estará num dia: `python ferramentas/gerar.py --ate AAAA-MM-DD` (depois rode de novo sem `--ate`, antes de enviar).
- Nome do arquivo: `AAAA-MM-DD-01-slug.json`, com a mesma data do campo `data`.

## Painel das artes (artes.html)

- Cada informativo tem um número (Nº 001, 002...) pela ordem de publicação. Post novo entra no fim da fila, então os números não mudam.
- O número vai no nome do arquivo baixado (ex.: `047-slug-instagram.jpg`). Na arte e no post ele não aparece.
- O painel mostra publicados e programados, com busca pelo número, pelo tema ou por palavra, e filtros por área e situação.
- Post que veio de uma postagem do Google Meu Negócio leva o campo `"google": N` no JSON (logo depois de `data`). No painel aparece "Google nº N", e a busca `G12` acha a postagem 12.

## Título da publicação e ISSN (decidido em 9/11/2026)

- Resposta do Centro Brasileiro do ISSN (IBICT) ao primeiro pedido: o título deve aparecer em destaque, igual e sem sinais gráficos no meio, no cabeçalho de todas as páginas, e a página principal deve ter links para Apresentação, Expediente, volume atual e volumes anteriores.
- O título é **Informativos Ferreira Advogados**. "Você sabia?" passou a ser o nome da seção de perguntas e respostas (aparece nas artes e na linha de topo da página principal).
- Designação numérica no formato exigido: Vol. 1 2026, Vol. 2 2027, um volume por ano civil. Cada volume tem página própria (`vol-1-2026.html`), e `volumes.html` reúne o volume atual e os anteriores.
- O ISSN só pode ser pedido depois que o Vol. 2 2027 estiver publicado. Quando for concedido, preencher a constante `ISSN` em `ferramentas/gerar.py`.

## Tema da semana (desde 22/11/2026)

Quando um assunto jurídico está muito forte na semana (lei nova, decisão do STJ, TST ou STF, mudança do INSS), o post ganha `"tema_semana": true` e `"fontes"` com 1 a 3 notícias de referência. Ele aparece no topo da página inicial como "Tema da semana" por 7 dias a partir da data, e a página do post leva o selo "Tema da semana". Sem `fontes`, o gerador recusa o post. O texto é nosso: nunca copiar a notícia, nunca citar nome de parte, nunca escolher caso criminal, político ou de pessoa famosa.
