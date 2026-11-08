# Padrão dos posts "Você sabia?"

Pesquisa feita em 8/11/2026 para definir que tipo de post atrai a atenção de possíveis clientes, como montar a estrutura e que cores, imagens, chamadas e funções cada post deve ter. Os geradores (`ferramentas/gerar.py`) e a tarefa automática seguem este documento.

Força da evidência: a maior parte do que existe sobre marketing jurídico vem de agências e fornecedores, sem amostra declarada. Onde o número for de fornecedor, isso está dito. As regras da OAB vêm das notas já conferidas no repositório `site-ferreira-advogados` (`docs/research_notes/.../regras_oab.md`).

## 1. Que tipo de post atrai possíveis clientes

- **Uma dúvida real por post, respondida logo no início.** As fontes convergem: o leitor chega com uma pergunta e procura a resposta, não uma apresentação do escritório. Escrever sobre o problema do leitor, sem jargão ([Sociosquares](https://www.sociosquares.com/blog/how-to-write-blog-posts-for-your-law-firm-that-actually-bring-in-clients/); [Lexicon Legal Content](https://www.lexiconlegalcontent.com/10-tips-to-help-legal-blog-writers-turn-readers-into-clients/)).
- **Título com as palavras que a pessoa digitaria no Google.** "Você sabia que...?" funciona como gancho, desde que o resto do título traga o termo de busca (pensão, divórcio, FGTS, herança) ([Hennessey](https://hennessey.com/blog/legal-blog-ideas-content-that-helps-law-firms-rank-and-convert/)).
- **Texto escaneável:** subtítulos claros, listas e parágrafos curtos, porque a leitura é no celular ([Forward Push](https://forwardpush.com/blog/how-to-structure-your-law-blog-to-attract-and-retain-clients/)).
- **Perguntas frequentes no fim** para responder as dúvidas seguintes do leitor e mantê-lo na página ([Edwards Legal Marketing](https://edwardslegalmarketing.com/law-firm-content-writing-that-converts-how-to-turn-educational-blogs-into-signed-cases/)).
- **Temas de Família que mais geram dúvida:** pensão (cálculo, revisão, atraso), guarda e convivência, divórcio com e sem filhos, partilha e regime de bens, inventário ([Advbox](https://advbox.com.br/blog/instagram-na-advocacia/); [TJPB](https://www.tjpb.jus.br/w/saiba-como-e-quando-solicitar-guarda-regulamenta%C3%A7%C3%A3o-de-visitas-e-pens%C3%A3o-aliment%C3%ADcia%C2%A0-1)).

## 2. Estrutura de cada post (nesta ordem)

1. Área e título "Você sabia que...?".
2. **Resposta curta** em destaque: a resposta em 1 ou 2 frases.
3. Linha com data, tempo de leitura e autor.
4. Corpo: "O que a lei prevê" (ou "O que foi decidido") e "Na prática", 250 a 450 palavras.
5. **Perguntas frequentes**: 2 ou 3 perguntas curtas, com resposta em tese.
6. Base legal e notícia de referência.
7. Aviso "Texto informativo e em tese".
8. **Quem escreve + contato**: foto do advogado, nome, OAB, formação, IBDFAM, áreas, atendimento, botão do WhatsApp.
9. **Leia também**: 3 informativos relacionados (mesma área primeiro).
10. Compartilhar no WhatsApp.
11. No celular, barra fixa no rodapé com o botão do WhatsApp.

## 3. Cores

- Não há estudo controlado sobre cor e confiança em sites jurídicos. O que existe é opinião de agência (paleta calma e limitada, bastante espaço em branco, uso consistente das cores da marca) ([pesquisa sobre cores](https://me-iclickmedia.gitbook.io/melinda/designing-for-trust-key-elements-for-law-firm-and-legal-websites)).
- **Decisão:** manter a identidade do site institucional (grafite, aço, prata e fundo claro), para o leitor reconhecer o escritório ao passar de um site ao outro. O verde aparece só no botão do WhatsApp, para ele se destacar.
- Observação: o CLAUDE.md do escritório cita a paleta navy, dourado e branco. O site no ar usa grafite e prata. Se a marca mudar, mudam os dois sites juntos.

## 4. Imagens

- **Foto real do advogado** perto do contato. Fornecedores relatam alta de 35% a 45% na conversão com fotos reais em vez de banco de imagens, em testes fora do setor jurídico. É indício, não prova ([AttorneySync](https://attorneysync.com/blog/photographs-real-lawyers-stock-images); [Custom Legal Marketing](https://custom.legal/practice-areas/personal-injury-law-firm-marketing/stock-photos-vs-ai-photos-vs-real-attorney-photos/)). A OAB permite foto, nome, OAB, formação e instituições (CED, art. 44, § 1º), e o TED-SP admitiu coluna com nome e foto do autor (16/10/2025).
- **Sem foto de banco** (martelo, balança genérica, casal brigando) e sem imagem de clientes.
- **Capa para compartilhar (1200 x 630, abaixo de 300 KB):** é a imagem que aparece quando o link é enviado no WhatsApp e no Facebook. O WhatsApp corta perto do quadrado, então o texto fica centralizado ([Screenhance](https://screenhance.com/blog/og-image-size-guide); [Andrew Baker](https://andrewbaker.ninja/2026/03/05/fix-thumbnail-previews-on-whatsapp-linkedin-x-guide/)).
- **Arte para o Instagram (1080 x 1350, formato 4:5):** a pergunta em letras grandes, para o Dr. Filipe publicar. Carrosséis educativos são os que mais recebem "salvar", segundo dados de fornecedores ([Socialinsider](https://socialinsider.io/blog/instagram-carousel-research)). Uma arte única já serve; carrossel de 3 a 7 telas é o próximo passo ([ACE Conteúdo](https://aceconteudodigital.com.br/como-criar-conteudo-juridico-instagram/)).

## 5. Chamada para o WhatsApp (CTA)

- **Onde:** no bloco "Quem escreve" ao fim do post e na barra fixa do celular. Botão flutuante não pode cobrir o conteúdo e precisa ser testado no celular ([Chatsac](https://chatsac.com/blog/botao-whatsapp-site/)).
- **Mensagem pronta** com o tema do post ("Li o informativo ..."), para a conversa começar com contexto ([Wati](https://www.wati.io/pt-br/blog/botao-do-whatsapp-como-adicionar-o-widget-do-whatsapp-ao-site/)).
- **Texto do botão:** "Conversar pelo WhatsApp". O WhatsApp é dado de contato permitido (Provimento 205/2021, art. 4º, § 3º), e informar as áreas de atuação também é permitido (CED, art. 44, § 1º).
- **Limite da OAB:** a Cartilha do CFOAB (2024) veda chamada à contratação. Ficam de fora "contrate", "garanta seu direito", "fale agora com um advogado" e "análise gratuita do seu caso". A frase "Para tirar dúvidas sobre este assunto ou agendar um atendimento, o contato é pelo WhatsApp" foi pedida pelo Dr. Filipe e está na faixa de risco **médio** das notas do escritório. Se quiser risco baixo, troque por "Contato do escritório pelo WhatsApp".

## 6. Outras funções

- **Tempo de leitura** e data visíveis.
- **Autor com credenciais** no post e nos dados estruturados (Article com autor Person). É o sinal de confiança mais recomendado para conteúdo jurídico, que o Google trata como YMYL ([Rankings.io](https://rankings.io/blog/eeat-ymyl-for-lawyers/)).
- **Leia também** com 3 links internos, para o leitor seguir no site.
- **Compartilhar no WhatsApp** com título e link.
- **Leveza:** a página inicial só tem texto; imagens grandes só na capa de compartilhamento, que o leitor não baixa ao abrir o site.
- **Para depois:** medir cliques no WhatsApp por post (hoje o site de informativos não mede nada e não usa cookies; medir exige atualizar uma política de privacidade).
