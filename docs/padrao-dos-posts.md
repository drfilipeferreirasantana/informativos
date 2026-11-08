# Padrão dos posts "Você sabia?"

Pesquisa feita em 8/11/2026 para definir que tipo de post atrai a atenção de possíveis clientes, como montar a estrutura e que cores, imagens, chamadas e funções cada post deve ter. Os geradores (`ferramentas/gerar.py`) e a tarefa automática seguem este documento.

Força da evidência: a maior parte do que existe sobre marketing jurídico vem de agências e fornecedores, sem amostra declarada. Onde o número for de fornecedor, isso está dito. As regras da OAB vêm das notas já conferidas no repositório `site-ferreira-advogados` (`docs/research_notes/.../regras_oab.md`).

## 1. Que tipo de post atrai possíveis clientes

- **Uma dúvida real por post, respondida logo no início.** As fontes convergem: o leitor chega com uma pergunta e procura a resposta, não uma apresentação do escritório. Escrever sobre o problema do leitor, sem jargão ([Sociosquares](https://www.sociosquares.com/blog/how-to-write-blog-posts-for-your-law-firm-that-actually-bring-in-clients/); [Lexicon Legal Content](https://www.lexiconlegalcontent.com/10-tips-to-help-legal-blog-writers-turn-readers-into-clients/)).
- **Título com as palavras que a pessoa digitaria no Google.** "Você sabia que...?" funciona como gancho, desde que o resto do título traga o termo de busca (pensão, divórcio, FGTS, herança) ([Hennessey](https://hennessey.com/blog/legal-blog-ideas-content-that-helps-law-firms-rank-and-convert/)).
- **Texto escaneável:** subtítulos claros, listas e parágrafos curtos, porque a leitura é no celular ([Forward Push](https://forwardpush.com/blog/how-to-structure-your-law-blog-to-attract-and-retain-clients/)).
- **Perguntas frequentes no fim** para responder as dúvidas seguintes do leitor e mantê-lo na página ([Edwards Legal Marketing](https://edwardslegalmarketing.com/law-firm-content-writing-that-converts-how-to-turn-educational-blogs-into-signed-cases/)).
- **Temas de Família que mais geram dúvida:** pensão (cálculo, revisão, atraso), guarda e convivência, divórcio com e sem filhos, partilha e regime de bens, inventário ([Advbox](https://advbox.com.br/blog/instagram-na-advocacia/); [TJPB](https://www.tjpb.jus.br/w/saiba-como-e-quando-solicitar-guarda-regulamenta%C3%A7%C3%A3o-de-visitas-e-pens%C3%A3o-aliment%C3%ADcia%C2%A0-1)).

## 2. Estrutura de cada post (formato visual, revisto em 8/11/2026)

O público lê pouco: a imagem e a resposta vêm primeiro, o texto fica opcional. O Dr. Filipe aparece em todo post como quem explica (foto, nome e assinatura), sem frases de autoelogio, que o Provimento 205/2021 veda.

1. **Capa com foto da área** em tela cheia, número do informativo, a pergunta "Você sabia que...?" em letras grandes e a assinatura com foto: "Dr. Filipe Ferreira explica".
2. **Resposta em 10 segundos:** selo curto em destaque (campo `destaque`, até 22 caracteres, ex.: "PRAZO: 7 DIAS") e a resposta em 1 ou 2 frases (`resumo`).
3. **Em 3 pontos:** cartões com ícone, número e uma frase cada (`pontos`).
4. **Situação do dia a dia:** um exemplo fictício, marcado como tal, para o leitor se reconhecer (`exemplo`). Nunca um caso real de cliente.
5. **Entenda melhor:** o texto completo, recolhido (`corpo`).
6. **Perguntas frequentes**, base legal e notícia de referência.
7. **Quem explica:** foto, nome, OAB, formação, IBDFAM, áreas do escritório e o botão "Conversar pelo WhatsApp".
8. **Você também pode gostar:** 3 informativos relacionados, com foto.
9. No celular, barra fixa com o botão do WhatsApp.

## 3. Cores

- Não há estudo controlado sobre cor e confiança em sites jurídicos; o que existe é opinião de agência (paleta calma e limitada, bastante espaço em branco, cores da marca usadas de forma consistente) ([pesquisa sobre cores](https://me-iclickmedia.gitbook.io/melinda/designing-for-trust-key-elements-for-law-firm-and-legal-websites)).
- **Decisão (pedido do Dr. Filipe em 8/11/2026):** combinar com o site do escritório sem copiar. **Marinho profundo** (#0f1b2d) para seriedade e confiança, **dourado discreto** (#b8935a) para competência, **off-white** (#f4f2ee) e cinzas neutros no texto. O verde aparece só nos botões do WhatsApp. A paleta coincide com a do CLAUDE.md do escritório (navy, dourado e branco).

## 4. Imagens

- **Foto real do advogado** perto do contato. Fornecedores relatam alta de 35% a 45% na conversão com fotos reais em vez de banco de imagens, em testes fora do setor jurídico. É indício, não prova ([AttorneySync](https://attorneysync.com/blog/photographs-real-lawyers-stock-images); [Custom Legal Marketing](https://custom.legal/practice-areas/personal-injury-law-firm-marketing/stock-photos-vs-ai-photos-vs-real-attorney-photos/)). A OAB permite foto, nome, OAB, formação e instituições (CED, art. 44, § 1º), e o TED-SP admitiu coluna com nome e foto do autor (16/10/2025).
- **Sem foto de banco** (martelo, balança genérica, casal brigando) e sem imagem de clientes.
- **Capa para compartilhar (1200 x 630, abaixo de 300 KB):** é a imagem que aparece quando o link é enviado no WhatsApp e no Facebook. O WhatsApp corta perto do quadrado, então o texto fica centralizado ([Screenhance](https://screenhance.com/blog/og-image-size-guide); [Andrew Baker](https://andrewbaker.ninja/2026/03/05/fix-thumbnail-previews-on-whatsapp-linkedin-x-guide/)).
- **Arte para o Instagram (1080 x 1350, formato 4:5):** foto da área, a pergunta em letras grandes, o destaque em dourado e a assinatura com a foto do Dr. Filipe. Todas as artes ficam na página `artes.html` (fora do Google), com botões para baixar e enviar no WhatsApp. Carrosséis educativos são os que mais recebem "salvar", segundo dados de fornecedores ([Socialinsider](https://socialinsider.io/blog/instagram-carousel-research)). Uma arte única já serve; carrossel de 3 a 7 telas é o próximo passo ([ACE Conteúdo](https://aceconteudodigital.com.br/como-criar-conteudo-juridico-instagram/)).

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
