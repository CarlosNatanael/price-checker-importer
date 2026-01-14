import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.converter import GenericConverter

def main():
    print("Iniciando importador Tanca/Jetway...")
    config_txt_pipe = {
        "layout_type": "delimited",
        "delimiter": "|", 
        "has_header": False,
        "map": {
            "ean": 0,
            "desc": 1,
            "price": 2
        }
    }
    config_txt_fixo = {
        "layout_type": "fixed_width",
        "has_header": False,
        "map": {
            "ean": (0, 13),   
            "desc": (13, 20), 
            "price": (33, 6)
        }
    }
    converter = GenericConverter()
    arquivo_entrada = "test.txt"
    arquivo_saida = "itens_para_vp.txt"
    qtd = converter.convert(arquivo_entrada, arquivo_saida, config_txt_pipe)
    
    if qtd > 0:
        print(f"Sucesso! Gerado '{arquivo_saida}' com {qtd} produtos.")
        print("Agora é só usar o uploader para enviar!")
    else:
        print("Nenhum produto convertido. Verifique o caminho do arquivo.")

if __name__ == "__main__":
    main()