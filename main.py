from common.df import df
from core.data_preparation import validar_padrao_df, transformar_df
from core.menus import menu

def main():
    validar_padrao_df()
    transformar_df()

    menu()

if __name__ == "__main__":
    main()