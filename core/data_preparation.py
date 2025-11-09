import pandas as pd

from common.df import df

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