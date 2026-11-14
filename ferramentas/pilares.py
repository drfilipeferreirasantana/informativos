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
              "imovel-do-ex-conjuge-moradia-dos-filhos", "reconhecimento-de-paternidade-dna"]),
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
}
