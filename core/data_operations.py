import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()

def operacao_estatisticas_descritivas(_dados_executar_operacao):
    dicionario_mapeamento = {
        "count": "Frequência absoluta",
        "mean": "Média",
        "std": "Desvio-padrão",
        "min": "Valor mínimo",
        "max": "Valor máximo",
        "25%": "Primeiro quartil",
        "50%": "Segundo quartil (Mediana)",
        "75%": "Terceiro quartil"
    }

    serie_estatisticas_descritivas_completa = pd.concat([
        _dados_executar_operacao.describe(include=[np.number]).rename(dicionario_mapeamento),
        pd.Series(_dados_executar_operacao["valor"].sum(), index=["Valor total"], name="valor")
    ])

    print(serie_estatisticas_descritivas_completa)

    from core.menus import menu # Lazy Import necessário para evitar Circular Import
    menu()

def operacao_boxplot(_dados_executar_operacao):
    sns.boxplot(_dados_executar_operacao, y="valor")
    plt.ylabel("Valor")

    print("\nFeche o gráfico em aberto para voltar ao menu.")
    plt.show()
    
    from core.menus import menu # Lazy Import necessário para evitar Circular Import
    menu()

def operacao_serie_temporal(_dados_executar_operacao):
    _dados_executar_operacao = _dados_executar_operacao.groupby(_dados_executar_operacao["data"].dt.to_period("M"))["valor"].sum().reset_index()
    _dados_executar_operacao["data"] = _dados_executar_operacao["data"].dt.to_timestamp() # Conversão necessária para datetime (seaborn não está preparado para Period Objects)

    sns.lineplot(data=_dados_executar_operacao, x="data", y="valor")
    plt.title("Evolução mensal do valor total")
    plt.xticks(_dados_executar_operacao["data"], _dados_executar_operacao["data"].dt.strftime("%Y-%m"), rotation=45)
    plt.xlabel("Ano-mês")
    plt.ylabel("Valor total")
    
    print("\nFeche o gráfico em aberto para voltar ao menu.")
    plt.show()
    
    from core.menus import menu # Lazy Import necessário para evitar Circular Import
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

    from core.menus import menu # Lazy Import necessário para evitar Circular Import
    menu()

def operacao_grafico_barras(_dados_executar_operacao):
    _dados_executar_operacao = _dados_executar_operacao.reset_index()
    colunas_df_executar_operacao = _dados_executar_operacao.columns.to_list()

    sns.barplot(data=_dados_executar_operacao, x=colunas_df_executar_operacao[0], y=colunas_df_executar_operacao[1])
    plt.xticks(rotation=45)

    print("\nFeche o gráfico em aberto para voltar ao menu.")
    plt.show()
    
    from core.menus import menu # Lazy Import necessário para evitar Circular Import
    menu()