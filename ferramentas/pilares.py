"""Páginas-pilar (guias completos por tema), pedidas pelo Dr. Filipe em 14/11/2026.

Um pilar explica o tema do começo ao fim e aponta para cada informativo do assunto. Para o Google,
mostra que o site cobre o tema por inteiro. Cada seção lista os informativos pelo slug: só aparecem
os já publicados; os programados entram sozinhos no dia em que forem ao ar.
"""

PILARES = {
    "divorcio": {
        "pagina": "divorcio.html",
        "area": "familia",
        "foto": "divorcio-sem-concordancia-do-outro",  # foto do topo e do cartão (assets/fotos/posts/)
        "titulo": "Divórcio: guia completo",
        "titulo_google": "Divórcio: como funciona, partilha de bens, guarda e pensão",
        "descricao": ("Guia completo do divórcio: quem pode pedir, cartório ou Justiça, partilha de bens conforme "
                      "o regime, guarda dos filhos, pensão alimentícia e união estável, com links para cada informativo."),
        "destaque": "Para se divorciar não é preciso motivo, prazo nem a concordância do outro.",
        "resumo": ("O que muda de um caso para outro é o caminho (cartório ou Justiça) e o que precisa ser decidido "
                   "junto: a divisão dos bens, a guarda e a convivência com os filhos e a pensão."),
        "atualizado": "2026-11-14",
        "secoes": [
            ("Quem pode pedir o divórcio?",
             ["Qualquer um dos cônjuges, a qualquer tempo. Desde a Emenda Constitucional 66/2010 não existe prazo "
              "mínimo de casamento nem de separação, e ninguém precisa provar culpa ou motivo.",
              "Se o outro não quiser, o divórcio sai do mesmo jeito, pela Justiça. A discordância pode atrasar a "
              "divisão dos bens ou a definição da guarda, mas não impede o fim do casamento."],
             ["divorcio-sem-concordancia-do-outro"]),
            ("Divórcio em cartório ou na Justiça?",
             ["Quando o casal está de acordo, o divórcio pode ser feito por escritura em cartório, com advogado, "
              "em poucos dias. Havendo filhos menores, o cartório é possível quando guarda, convivência e pensão "
              "já foram resolvidas na Justiça.",
              "Sem acordo, o caminho é a ação de divórcio. O juiz pode decretar o divórcio logo no início e "
              "deixar a partilha e as questões dos filhos para seguir depois."],
             ["divorcio-em-cartorio-com-filhos-menores", "divorcio-sem-partilha-de-bens"]),
            ("Como fica a partilha de bens?",
             ["Depende do regime de bens. Na comunhão parcial, que vale para quem casou sem pacto, divide-se pela "
              "metade o que foi comprado durante o casamento. Ficam de fora os bens de antes do casamento e o que "
              "cada um recebeu por herança ou doação.",
              "Entram na conta também o FGTS depositado durante o casamento, as dívidas feitas em favor da família, "
              "a parte paga do imóvel financiado e as quotas de empresa. A separação de fato marca o fim dessa "
              "comunhão: o que cada um compra depois, em regra, não se divide."],
             ["regimes-de-bens-qual-a-diferenca", "fgts-entra-na-partilha-do-divorcio",
              "heranca-na-partilha-do-divorcio", "imovel-financiado-antes-do-casamento-partilha",
              "dividas-do-casal-no-divorcio", "separacao-de-fato-bens-depois",
              "mudar-regime-de-bens-depois-de-casado"]),
            ("E quando há empresa, imóveis ou investimentos?",
             ["As quotas de sociedade compradas durante o casamento entram na partilha pelo valor, mesmo que o outro "
              "cônjuge não vire sócio. Aluguéis e lucros recebidos durante o casamento também podem ser divididos, "
              "ainda que venham de bens anteriores.",
              "Se houver suspeita de bens passados para o nome da empresa ou de terceiros, a Justiça pode investigar "
              "e trazer esses bens de volta para a partilha."],
             ["divorcio-socio-de-empresa-quotas-na-partilha", "alugueis-e-lucros-entram-na-partilha",
              "bens-escondidos-na-empresa-no-divorcio", "pacto-antenupcial-e-contrato-de-convivencia"]),
            ("Como ficam os filhos?",
             ["A guarda compartilhada é a regra, mesmo quando os pais não se entendem. Ela divide as decisões sobre a "
              "vida da criança; a moradia pode ser fixada com um dos pais, com convivência ampla com o outro.",
              "Impedir o contato com o outro genitor ou falar mal dele para a criança pode configurar alienação "
              "parental, que a lei manda coibir."],
             ["guarda-compartilhada-e-a-regra", "genitor-impede-contato-com-o-filho-alienacao-parental",
              "imovel-do-ex-conjuge-moradia-dos-filhos"]),
            ("Como funciona a pensão alimentícia?",
             ["Não existe percentual fixo em lei. O valor equilibra a necessidade de quem recebe e a possibilidade de "
              "quem paga, e pode ser revisto quando a situação de um dos dois muda.",
              "A pensão não acaba sozinha aos 18 anos: o fim depende de decisão judicial, e o filho que estuda pode "
              "continuar recebendo. A pensão atrasada pode levar à prisão civil de quem deve."],
             ["valor-da-pensao-alimenticia", "revisao-do-valor-da-pensao", "pensao-nao-acaba-automaticamente-aos-18",
              "pensao-filho-na-faculdade", "prisao-por-pensao-atrasada", "avos-podem-pagar-pensao",
              "alimentos-gravidicos-pensao-na-gravidez"]),
            ("E na união estável?",
             ["Sem contrato escrito, a união estável segue as regras da comunhão parcial: o que foi comprado durante a "
              "convivência é dividido na separação. Guarda e pensão dos filhos seguem as mesmas regras do casamento."],
             ["uniao-estavel-divisao-de-bens", "pacto-antenupcial-e-contrato-de-convivencia"]),
        ],
        "documentos": ["Certidão de casamento atualizada (ou prova da união estável)",
                       "Documentos pessoais do casal e certidão de nascimento dos filhos",
                       "Lista dos bens e das dívidas, com documentos (matrículas, contratos, extratos)",
                       "Comprovantes de renda, para a discussão da pensão"],
        "faq": [
            ("Preciso de advogado para me divorciar?",
             "Sim. No cartório a lei exige a presença de advogado na escritura; na Justiça, o pedido também é feito por advogado."),
            ("Quanto tempo demora um divórcio?",
             "Em cartório, com tudo de acordo, costuma levar poucos dias. Na Justiça, o divórcio pode ser decretado no início, e o tempo maior fica para a partilha e as questões dos filhos quando há disputa."),
            ("Quem sai de casa perde o direito aos bens?",
             "Em regra, não: sair de casa não tira a metade dos bens comuns, e a separação de fato só encerra a comunhão para o que for comprado depois. A exceção é o abandono do lar: quem deixa o imóvel urbano do casal e a família por 2 anos pode perder a sua parte para o outro (Código Civil, art. 1.240-A)."),
            ("Posso me divorciar e dividir os bens depois?",
             "Sim. A lei permite o divórcio sem a partilha, que pode ser feita depois, por acordo ou na Justiça."),
        ],
        "base": ["Constituição Federal, art. 226, § 6º (Emenda Constitucional 66/2010)",
                 "Código Civil, arts. 1.571 a 1.582, 1.583 a 1.590, 1.658 a 1.666, 1.694 a 1.710 e 1.725",
                 "Código Civil, art. 1.240-A (usucapião familiar)",
                 "Código de Processo Civil, arts. 528, 693 a 699 e 733",
                 "Lei 12.318/2010 (alienação parental)", "Súmula 358 do STJ"],
    },
    "pensao": {
        "pagina": "pensao-alimenticia.html",
        "area": "familia",
        "foto": "valor-da-pensao-alimenticia",
        "titulo": "Pensão alimentícia: guia completo",
        "titulo_google": "Pensão alimentícia: quem tem direito, valor, até quando e o que fazer no atraso",
        "descricao": ("Guia completo da pensão alimentícia: quem tem direito, como o valor é definido, pensão na gravidez, "
                      "avós, até quando é paga, revisão e o que fazer quando atrasa, com links para cada informativo."),
        "destaque": "Não existe percentual fixo de pensão em lei.",
        "resumo": ("O valor é definido caso a caso, pela necessidade de quem recebe e pela possibilidade de quem paga, "
                   "e pode ser revisto sempre que a situação de um dos dois mudar."),
        "atualizado": "2026-11-14",
        "secoes": [
            ("Quem tem direito à pensão?",
             ["Os filhos menores têm direito à pensão dos pais, que devem sustentá-los. A obrigação também existe entre "
              "outros parentes, como pais idosos e netos, conforme a necessidade de um e a possibilidade do outro.",
              "O ex-cônjuge ou ex-companheiro pode receber pensão em situação excepcional, quando não tem como se "
              "sustentar sozinho. Em regra, ela é temporária, pelo tempo necessário para a pessoa voltar ao mercado de trabalho."],
             []),
            ("Como o valor é definido?",
             ["O juiz equilibra três pontos: o que o filho precisa (escola, saúde, alimentação, moradia), o que quem paga "
              "pode pagar e a proporção da renda de cada um dos pais. A ideia de que a pensão é sempre 30% do salário não está na lei.",
              "Quando quem paga é autônomo ou esconde a renda, contam os sinais de riqueza: carro, viagens, padrão de "
              "vida e o que aparece nas redes sociais. Para quem tem carteira assinada, o valor pode ser descontado direto do salário."],
             ["valor-da-pensao-alimenticia"]),
            ("Dá para pedir pensão na gravidez ou antes do reconhecimento da paternidade?",
             ["Sim. A gestante pode pedir alimentos gravídicos para as despesas da gravidez, com base em indícios da "
              "paternidade. Depois do nascimento, eles viram pensão para o filho.",
              "Quando o pai não reconhece o filho, a ação de investigação de paternidade pode vir junto com o pedido de "
              "pensão. Quem se recusa a fazer o exame de DNA tem a paternidade presumida."],
             ["alimentos-gravidicos-pensao-na-gravidez", "reconhecimento-de-paternidade-dna"]),
            ("Se o pai ou a mãe não pode pagar, os avós pagam?",
             ["Os avós podem ser chamados, mas só de forma complementar: quando os pais não pagam ou pagam menos do que o "
              "filho precisa. Antes, é preciso mostrar que se tentou cobrar de quem deve em primeiro lugar."],
             ["avos-podem-pagar-pensao"]),
            ("Até quando a pensão é paga?",
             ["A pensão não acaba sozinha quando o filho faz 18 anos. Para parar de pagar, é preciso pedir à Justiça a "
              "exoneração, e o filho tem a chance de mostrar que ainda precisa.",
              "O filho que estuda, em faculdade ou curso técnico, costuma continuar recebendo até o fim do curso. Os "
              "tribunais usam com frequência a idade de 24 anos como referência."],
             ["pensao-nao-acaba-automaticamente-aos-18", "pensao-filho-na-faculdade"]),
            ("Dá para aumentar ou diminuir a pensão?",
             ["Sim, quando a situação muda: o filho passa a ter gastos maiores, quem paga passa a ganhar mais, perde o "
              "emprego ou tem outro filho. O pedido é feito em ação revisional, e o valor só muda com decisão ou acordo homologado.",
              "Enquanto isso, o valor antigo continua valendo. Parar de pagar por conta própria gera dívida e pode levar à prisão."],
             ["revisao-do-valor-da-pensao"]),
            ("E se a pensão atrasar?",
             ["A pensão atrasada pode ser cobrada na Justiça. Para as três últimas parcelas vencidas antes da cobrança e as "
              "que vencerem durante o processo, cabe a prisão civil de 1 a 3 meses de quem deve.",
              "Também são possíveis a penhora de bens e salário, o protesto da dívida, a inclusão do nome em cadastro de "
              "inadimplentes e, em alguns casos, a suspensão da carteira de motorista e do passaporte."],
             ["prisao-por-pensao-atrasada"]),
        ],
        "documentos": ["Certidão de nascimento do filho",
                       "Comprovantes dos gastos do filho: escola, plano de saúde, remédios, alimentação, moradia",
                       "O que souber da renda de quem paga: emprego, holerite, bens, padrão de vida",
                       "Decisão ou acordo de pensão anterior, se houver, e o controle dos pagamentos"],
        "faq": [
            ("A pensão é sempre 30% do salário?",
             "Não. A lei não fixa percentual. O valor depende da necessidade do filho e da possibilidade de quem paga, e 30% é só um número que aparece em muitos acordos."),
            ("Quem está desempregado precisa pagar pensão?",
             "Sim. O desemprego não acaba com a obrigação. Ele pode justificar um pedido de revisão do valor, mas parar de pagar por conta própria gera dívida."),
            ("A pensão pode ser descontada direto do salário?",
             "Sim. Quando quem paga tem carteira assinada ou é servidor, o juiz pode mandar a empresa descontar a pensão na folha e depositar direto para o filho."),
            ("Ex-mulher ou ex-marido tem direito a pensão?",
             "Só em situação excepcional, quando não consegue se sustentar sozinho. Em regra, a pensão entre ex-cônjuges é temporária."),
        ],
        "base": ["Constituição Federal, art. 229",
                 "Código Civil, arts. 1.694 a 1.710",
                 "Lei 5.478/1968 (Lei de Alimentos) e Lei 11.804/2008 (alimentos gravídicos)",
                 "Código de Processo Civil, arts. 139, IV, e 528 a 533",
                 "Súmulas 301, 309, 358 e 596 do STJ"],
    },
}
