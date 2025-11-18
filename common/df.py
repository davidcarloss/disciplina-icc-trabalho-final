import pandas as pd

caminho_arquivo = "./dummy_data1.csv"
"""
Cenário sucesso:
- Número de colunas igual ao esperado;
- Colunas esperadas estão presentes;
- Dtypes de cada coluna são adequados.
"""

# caminho_arquivo = "./dummy_data2.csv"
"""
Cenário erro:
- Número de colunas diferente do esperado;
- Colunas Gasto não presente e Fonte Pagamento com nome errado;
- Dtypes das colunas válidas são adequados.
"""

# caminho_arquivo = "./dummy_data3.csv"
"""
Cenário erro:
- Número de colunas igual ao esperado;
- Colunas esperadas estão presentes;
- Dtype inválido da coluna Fonte Pagamento.
"""

if not caminho_arquivo[-4:] == ".csv":
    print("[Erro] O arquivo especificado precisa ter a extensão '.csv'.")
    exit(1)
else:
    try:
        df = pd.read_csv(caminho_arquivo)
    except:
        print("[Erro] Falha ao carregar arquivo especificado.")
        exit(1)