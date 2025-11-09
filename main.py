import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()

caminho_arquivo = "./gastos.csv"

df = pd.read_csv(caminho_arquivo)

colunas_tipos_esperados_df = {
    "Gasto": ["object"],
    "Categorias": ["object"],
    "Valor": ["object", "float64", "float32", "float16", "int64", "int32", "int16", "int8"],
    "Data": ["object", "datetime64[ns]"],
    "Fonte Pagamento": ["object"],
    "Forma Pagamento": ["object"]
}

def validar_padrao_df():
    def colunas_validas():
        valido = True

        colunas_csv = df.columns.to_list()

        if len(colunas_csv) != len(colunas_tipos_esperados_df):
            print("[Erro][Validação] Número de colunas diferente do esperado.")
            valido = False

        for coluna_esperada in colunas_tipos_esperados_df:
            if coluna_esperada not in colunas_csv:
                print(f"[Erro][Validação] Coluna {coluna_esperada} não encontrada.")
                valido = False

        return valido

    def tipos_validos():
        valido = True

        for coluna_esperada, tipos_aceitos in colunas_tipos_esperados_df.items():
            if df.get(coluna_esperada, default=None) is not None:
                coluna_df_tipo = df[coluna_esperada].dtype

                if not coluna_df_tipo in tipos_aceitos:
                    print(f"[Erro][Validação] Tipo {coluna_df_tipo} não aceito na coluna {coluna_esperada}.")
                    valido = False

        return valido

    df_valido = all([colunas_validas(), tipos_validos()])

    if not df_valido:
        print("DataFrame inválido.")
        exit(1)
    else:
        print("DataFrame válido.")

def transformar_df():
    def renomeia_colunas():
        dicionario_mapeamento = {
            "Gasto": "gasto",
            "Categorias": "categoria",
            "Valor": "valor",
            "Data": "data",
            "Fonte Pagamento": "fonte_pagamento",
            "Forma Pagamento": "forma_pagamento"
        }

        df.rename(columns=dicionario_mapeamento, inplace=True)

    def converte_dados():
        df["categoria"] = df["categoria"].apply(lambda e: [s.strip() for s in e.split(",")])
        
        if df["valor"].dtype == "object":
            df["valor"] = pd.to_numeric(df["valor"].str.strip().str.replace("R$", "").str.replace(".", "").str.replace(",", "."), errors="coerce")

        if df["data"].dtype == "object":
            data_convertida_dia_primeiro = pd.to_datetime(df["data"], dayfirst=True, errors="coerce")
            data_convertida_mes_primeiro = pd.to_datetime(df["data"], dayfirst=False, errors="coerce")

            if data_convertida_dia_primeiro.isna().sum() < data_convertida_mes_primeiro.isna().sum():
                df["data"] = data_convertida_dia_primeiro
            else:
                df["data"] = data_convertida_mes_primeiro

    renomeia_colunas()
    converte_dados()

def operacao_estatisticas_descritivas(_dados_executar_operacao):
    dicionario_mapeamento = {
        "count": "Frequência absoluta",
        "mean": "Média",
        "std": "Desvio-padrão",
        "min": "Valor mínimo",
        "max": "Valor máximo",
        "25%": "Primeiro quartil",
        "50%": "Segundo quartil",
        "75%": "Terceiro quartil"
    }

    serie_estatisticas_descritivas_completa = pd.concat([
        _dados_executar_operacao.describe(include=[np.number]).rename(dicionario_mapeamento),
        pd.Series(_dados_executar_operacao["valor"].sum(), index=["Valor total"], name="valor")
    ])

    print(serie_estatisticas_descritivas_completa)

    menu()

def operacao_boxplot(_dados_executar_operacao):
    sns.boxplot(_dados_executar_operacao, y="valor")
    plt.ylabel("Valor")

    print("\nFeche o gráfico em aberto para voltar ao menu.")
    plt.show()
    
    menu()

def operacao_serie_temporal(_dados_executar_operacao):
    _dados_executar_operacao = _dados_executar_operacao.groupby(_dados_executar_operacao["data"].dt.to_period("M"))["valor"].sum().reset_index()
    _dados_executar_operacao["data"] = _dados_executar_operacao["data"].dt.to_timestamp() # Converte Period objects

    sns.lineplot(data=_dados_executar_operacao, x="data", y="valor")
    plt.title("Evolução mensal do valor total")
    plt.xticks(_dados_executar_operacao["data"], _dados_executar_operacao["data"].dt.strftime("%Y-%m"), rotation=45)
    plt.xlabel("Ano-mês")
    plt.ylabel("Valor total")
    
    print("\nFeche o gráfico em aberto para voltar ao menu.")
    plt.show()
    
    menu()

def operacao_tabela_frequencias(_dados_executar_operacao):
    serie_escolhida = None

    def tabela_frequencias_ano_mes():
        nonlocal serie_escolhida
        serie_escolhida = _dados_executar_operacao["data"].dt.to_period("M")

    def tabela_frequencias_categoria():
        nonlocal serie_escolhida
        serie_escolhida = _dados_executar_operacao.explode("categoria", ignore_index=True)["categoria"]

    def tabela_frequencias_fonte_pagamento():
        nonlocal serie_escolhida
        serie_escolhida = _dados_executar_operacao["fonte_pagamento"]

    def tabela_frequencias_forma_pagamento():
        nonlocal serie_escolhida
        serie_escolhida = _dados_executar_operacao["forma_pagamento"]
    
    opcoes_tabela_frequencias = [
        ("1", { "texto_exibicao": "Ano-mês", "funcao": tabela_frequencias_ano_mes }),
        ("2", { "texto_exibicao": "Categoria", "funcao": tabela_frequencias_categoria }),
        ("3", { "texto_exibicao": "Fonte de Pagamento", "funcao": tabela_frequencias_fonte_pagamento }),
        ("4", { "texto_exibicao": "Forma de Pagamento", "funcao": tabela_frequencias_forma_pagamento }),
    ]

    print("\nEscolha a tabela:")

    for opcao, configuracao in opcoes_tabela_frequencias:
        print(f"{opcao}. {configuracao["texto_exibicao"]}")

    escolha_usuario = input()

    configuracao_opcao_escolhida = next((configuracao for opcao, configuracao in opcoes_tabela_frequencias if opcao == escolha_usuario), None)

    if configuracao_opcao_escolhida == None:
        print("\n[Aviso] Inválida.")
        menu()
    else:
        configuracao_opcao_escolhida["funcao"]()

        frequencia_absoluta = serie_escolhida.value_counts()
        frequencia_relativa = serie_escolhida.value_counts(normalize=True)
        frequencia_acumulada = frequencia_absoluta.cumsum()
        frequencia_relativa_acumulada = frequencia_relativa.cumsum()

        df_frequencias = pd.DataFrame({
            "Frequência Absoluta": frequencia_absoluta,
            "Frequência Relativa (%)": (frequencia_relativa * 100).round(2),
            "Frequência Acumulada": frequencia_acumulada,
            "Frequência Relativa Acumulada (%)": (frequencia_relativa_acumulada * 100).round(2)
        })

        print(df_frequencias)
        menu()

def operacao_grafico_barras(_dados_executar_operacao):
    _dados_executar_operacao = _dados_executar_operacao.reset_index()
    colunas_df_executar_operacao = _dados_executar_operacao.columns.to_list()

    sns.barplot(data=_dados_executar_operacao, x=colunas_df_executar_operacao[0], y=colunas_df_executar_operacao[1])
    plt.xticks(rotation=45)

    print("\nFeche o gráfico em aberto para voltar ao menu.")
    plt.show()
    
    menu()

def menu_operacoes(_nivel_operacao, dados_executar_operacao):
    print("\nEscolha a operação a executar:")

    operacoes_disponiveis = next((configuracao for opcao, configuracao in opcoes_menu_principal if opcao == _nivel_operacao))["operacoes_disponiveis"]
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
    print("\nEscolha o nível do Dataframe para executar as operações:")
    for opcao, configuracao in opcoes_menu_principal:
        print(f"{opcao}. {configuracao["texto_exibicao"]}")
    
    escolha_usuario = input()

    configuracao_opcao_escolhida = next((configuracao for opcao, configuracao in opcoes_menu_principal if opcao == escolha_usuario), None)

    if configuracao_opcao_escolhida == None:
        print("\n[Aviso] Inválida.")
        menu()
    else:
        configuracao_opcao_escolhida["funcao"]()

def iniciar():
    validar_padrao_df()
    transformar_df()

    menu()

iniciar()