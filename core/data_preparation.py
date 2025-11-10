import pandas as pd

from common.df import df

# Dicionário que especifica as colunas esperadas, e seus respectivos dtypes permitidos, do arquivo CSV
colunas_tipos_esperados_df = {
    "Gasto": ["object"],
    "Categorias": ["object"],
    "Valor": ["object", "float64", "float32", "float16", "int64", "int32", "int16", "int8"],
    "Data": ["object", "datetime64[ns]"],
    "Fonte Pagamento": ["object"],
    "Forma Pagamento": ["object"]
}

def validar_padrao_df():
    
    # Valida se as colunas são as esperadas
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

    # Valida se os tipos são os permitidos
    def tipos_validos():
        valido = True

        for coluna_esperada, tipos_aceitos in colunas_tipos_esperados_df.items():
            if df.get(coluna_esperada, default=None) is not None:
                coluna_df_tipo = df[coluna_esperada].dtype

                if not coluna_df_tipo in tipos_aceitos:
                    print(f"[Erro][Validação] Tipo {coluna_df_tipo} não aceito na coluna {coluna_esperada}.")
                    valido = False

        return valido

    # É válido somente se todas as funções de validação 'passarem'
    df_valido = all([colunas_validas(), tipos_validos()])

    if not df_valido:
        print("DataFrame inválido.")
        exit(1)
    else:
        print("DataFrame válido.")

def transformar_df():
    
    # Renomeia as colunas do DF para melhor manipulação 
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

    # Conversão de dtypes das colunas
    def converte_dados():
        
        # Transforma strings de formato "Categoria1, Categoria2, ..., CategoriaN" em uma lista ["Categoria1", "Categoria2", ..., "CategoriaN"].
        # Exemplo: "Transporte, Uber" em ["Transporte", "Uber"]
        df["categoria"] = df["categoria"].apply(lambda e: [s.strip() for s in e.split(",")])
        
        # Caso coluna Valor seja string (assume padrão brasileiro), converte para float ou int
        if df["valor"].dtype == "object":
            df["valor"] = pd.to_numeric(df["valor"].str.strip().str.replace("R$", "").str.replace(".", "").str.replace(",", "."), errors="coerce")

        # Caso coluna Data seja string, converte para datetime
        if df["data"].dtype == "object":
            formatos_data_aceitos = ["%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%d-%m-%Y", "%m-%d-%Y", "%Y-%m-%d"] # Padrão strftime

            mapeamento_formato_data_total_nulas = {}

            for i, formato in enumerate(formatos_data_aceitos):
                mapeamento_formato_data_total_nulas[i] = pd.to_datetime(df["data"], format=formato, errors="coerce").isna().sum()

            formato_menor_total_nulas = min(mapeamento_formato_data_total_nulas, key=mapeamento_formato_data_total_nulas.get)

            df["data"] = pd.to_datetime(df["data"], format=formatos_data_aceitos[formato_menor_total_nulas], errors="coerce") # Converte coluna Data com formato que teve menor total de erros         
    
    renomeia_colunas()
    converte_dados()