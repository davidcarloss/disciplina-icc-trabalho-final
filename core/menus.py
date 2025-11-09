from common.df import df
from core.data_operations import operacao_estatisticas_descritivas, operacao_boxplot, operacao_serie_temporal, operacao_tabela_frequencias, operacao_grafico_barras

# As opções do Menu Operações são de acordo com o nível selecionado do DF
def menu_operacoes(_nivel_df, dados_executar_operacao):
    print("\nEscolha a operação a executar:")

    operacoes_disponiveis = next((configuracao for opcao, configuracao in opcoes_menu_principal if opcao == _nivel_df))["operacoes_disponiveis"]
    for opcao, configuracao in operacoes_disponiveis:
        print(f"{opcao}. {configuracao["texto_exibicao"]}")

    escolha_usuario = input()

    configuracao_opcao_escolhida = next((configuracao for opcao, configuracao in operacoes_disponiveis if opcao == escolha_usuario), None)

    if configuracao_opcao_escolhida == None:
        print("\n[Aviso] Inválida.")
        menu()
    else:
        configuracao_opcao_escolhida["funcao"](dados_executar_operacao)

def criterio_selecao_opcao1():
    print("Digite o Ano (no formato YYYY)")
    ano_selecionado = input()
    print("Digite o Mês (no formato MM)")
    mes_selecionado = input()

    try:
        ano_selecionado = int(ano_selecionado)
        mes_selecionado = int(mes_selecionado)
    except ValueError:
        print("\n[Aviso] Ano ou mês digitado não é um número inteiro.")
        menu()

    df_executar_operacao = df[(df["data"].dt.year == ano_selecionado) & (df["data"].dt.month == mes_selecionado)]
    menu_operacoes("2", df_executar_operacao)

def criterio_selecao_opcao2():
    print("Digite a Categoria (case sensitive)")
    categoria_selecionada = input()

    df_executar_operacao = df[df["categoria"].apply(lambda e: categoria_selecionada in e)]
    menu_operacoes("2", df_executar_operacao)

def criterio_selecao_opcao3():
    print("Digite a Fonte de Pagamento (case sensitive)")
    fonte_pagamento_selecionado = input()
    
    df_executar_operacao = df[df["fonte_pagamento"] == fonte_pagamento_selecionado]
    menu_operacoes("2", df_executar_operacao)

def criterio_selecao_opcao4():
    print("Digite a Forma de Pagamento (case sensitive)")
    forma_pagamento_selecionada = input()
    
    df_executar_operacao = df[df["forma_pagamento"] == forma_pagamento_selecionada]
    menu_operacoes("2", df_executar_operacao)

# Lista de opções do Submenu Seleção
opcoes_criterio_selecao = [
    ("1", { "texto_exibicao": "Ano-mês", "funcao": criterio_selecao_opcao1 }),
    ("2", { "texto_exibicao": "Categoria", "funcao": criterio_selecao_opcao2 }),
    ("3", { "texto_exibicao": "Fonte de Pagamento", "funcao": criterio_selecao_opcao3 }),
    ("4", { "texto_exibicao": "Forma de Pagamento", "funcao": criterio_selecao_opcao4 })
]

def criterio_agrupamento_opcao1():
    serie_executar_operacao = df.groupby(df["data"].dt.to_period("M"))["valor"].sum()

    menu_operacoes("3", serie_executar_operacao)

def criterio_agrupamento_opcao2():
    serie_executar_operacao = df.explode("categoria", ignore_index=True).groupby("categoria")["valor"].sum()

    menu_operacoes("3", serie_executar_operacao)

def criterio_agrupamento_opcao3():
    serie_executar_operacao = df.groupby("fonte_pagamento")["valor"].sum()

    menu_operacoes("3", serie_executar_operacao)

def criterio_agrupamento_opcao4():
    serie_executar_operacao = df.groupby("forma_pagamento")["valor"].sum()

    menu_operacoes("3", serie_executar_operacao)

# Lista de opções do Submenu Agrupamento
opcoes_criterio_agrupamento = [
    ("1", { "texto_exibicao": "Ano-mês", "funcao": criterio_agrupamento_opcao1 }),
    ("2", { "texto_exibicao": "Categoria", "funcao": criterio_agrupamento_opcao2 }),
    ("3", { "texto_exibicao": "Fonte de Pagamento", "funcao": criterio_agrupamento_opcao3 }),
    ("4", { "texto_exibicao": "Forma de Pagamento", "funcao": criterio_agrupamento_opcao4 })
]

def submenu_opcao1():
    menu_operacoes("1", df)

def submenu_opcao2():
    print("\nEscolha o critério de seleção:")
    for opcao, configuracao in opcoes_criterio_selecao:
        print(f"{opcao}. {configuracao["texto_exibicao"]}")

    escolha_usuario = input()

    configuracao_opcao_escolhida = next((configuracao for opcao, configuracao in opcoes_criterio_selecao if opcao == escolha_usuario), None)

    if configuracao_opcao_escolhida == None:
        print("\n[Aviso] Inválida.")
        menu()
    else:
        configuracao_opcao_escolhida["funcao"]()

def submenu_opcao3():
    print("\nEscolha o critério de agrupamento:")
    for opcao, configuracao in opcoes_criterio_agrupamento:
        print(f"{opcao}. {configuracao["texto_exibicao"]}")

    escolha_usuario = input()

    configuracao_opcao_escolhida = next((configuracao for opcao, configuracao in opcoes_criterio_agrupamento if opcao == escolha_usuario), None)

    if configuracao_opcao_escolhida == None:
        print("\n[Aviso] Inválida.")
        menu()
    else:
        configuracao_opcao_escolhida["funcao"]()

def submenu_opcao4():
    exit(0)

# Lista de opções do Menu Principal. Cada opção tem um texto de exibição, a função responsável e as operações que podem ser executadas
opcoes_menu_principal = [
    ("1", {
        "texto_exibicao": "Completo",
        "funcao": submenu_opcao1,
        "operacoes_disponiveis": [
            ("1", { "texto_exibicao": "Estatísticas descritivas", "funcao": operacao_estatisticas_descritivas }),
            ("2", { "texto_exibicao": "Boxplot", "funcao": operacao_boxplot }),
            ("3", { "texto_exibicao": "Série temporal", "funcao": operacao_serie_temporal }),
            ("4", { "texto_exibicao": "Tabela de frequências", "funcao": operacao_tabela_frequencias })
        ]
    }),
    ("2", {
        "texto_exibicao": "Selecionado por critério",
        "funcao": submenu_opcao2,
        "operacoes_disponiveis": [
            ("1", { "texto_exibicao": "Estatísticas descritivas", "funcao": operacao_estatisticas_descritivas }),
            ("2", { "texto_exibicao": "Boxplot", "funcao": operacao_boxplot })
        ]
    }),
    ("3", {
        "texto_exibicao": "Agrupado por critério",
        "funcao": submenu_opcao3,
        "operacoes_disponiveis": [
            ("1", { "texto_exibicao": "Gráfico de barras", "funcao": operacao_grafico_barras })
        ]
    }),
    ("0", {
        "texto_exibicao": "Sair",
        "funcao": submenu_opcao4
    })
]

def menu():
    """
    'Nível' se refere ao subconjunto do DF:
    - Completo sendo o DF inteiro;
    - Selecionado sendo um "recorte" do DF com base em algum critério;
    - Agrupado sendo uma Série da coluna Valor com base em algum critério.
    """
    print("\nEscolha o nível do Dataframe para aplicar as operações:")
    
    # Estrutura de repetição for para exibição das opções do Menu Principal
    for opcao, configuracao in opcoes_menu_principal:
        print(f"{opcao}. {configuracao["texto_exibicao"]}")
    
    escolha_usuario = input() # Opção escolhida pelo usuário

    # Função next utilizada para 'pular' laço for após primeira ocorrência da opção escolhida. Caso não tenha ocorrência retorna None
    configuracao_opcao_escolhida = next((configuracao for opcao, configuracao in opcoes_menu_principal if opcao == escolha_usuario), None)

    if configuracao_opcao_escolhida == None:
        print("\n[Aviso] Inválida.")
        menu()
    else:
        # Executa função responsável pela opção escolhida
        configuracao_opcao_escolhida["funcao"]()

    # Demais Menus e Submenus implementam solução análoga