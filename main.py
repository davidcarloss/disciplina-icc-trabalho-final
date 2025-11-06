import pandas as pd
import seaborn as sns

caminho_arquivo = "./gastos.csv"

df = pd.read_csv(caminho_arquivo)


def validar_padrao_df():
    def colunas_validas():
        valido = True

        colunas_esperadas = ["Gasto", "Categorias", "Valor", "Data", "Fonte Pagamento", "Forma Pagamento",
        ]
        colunas_csv = df.columns.to_list()

        if len(colunas_csv) != len(colunas_esperadas):
            valido = False

        for coluna_esperada in colunas_esperadas:
            if coluna_esperada not in colunas_csv:
                valido = False

        return valido

    df_valido = all([colunas_validas()])

    if not df_valido:
        print("O arquivo CSV não gerou um DataFrame válido.")
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
            "Forma Pagamento": "forma_pagamento",
        }

        df.rename(columns=dicionario_mapeamento, inplace=True)

    def converte_dados():
        df["categoria"] = df["categoria"].apply(lambda e: [s.strip() for s in e.split(",")])
        df["valor"] = pd.to_numeric(
            df["valor"].str.strip().str.replace("R$", "").str.replace(".", "").str.replace(",", "."),
            errors="coerce"
        )

        data_convertida_dia_primeiro = pd.to_datetime(df["data"], dayfirst=True, errors="coerce")
        data_convertida_mes_primeiro = pd.to_datetime(df["data"], dayfirst=False, errors="coerce")

        if data_convertida_dia_primeiro.isna().sum() < data_convertida_mes_primeiro.isna().sum():
            df["data"] = data_convertida_dia_primeiro
        else:
            df["data"] = data_convertida_mes_primeiro

    renomeia_colunas()
    converte_dados()


def iniciar():
    validar_padrao_df()
    transformar_df()

iniciar()
