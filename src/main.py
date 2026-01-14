# src/main.py
import sys
import os

# --- CORREÇÃO DO ERRO DE IMPORTAÇÃO ---
# Adiciona a pasta raiz do projeto ao caminho do Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.converter import GenericConverter

def main():
    print("🚀 Iniciando importador Tanca/Jetway...")
    
    # EXEMPLO 1: Lendo um TXT separado por PIPE (|)
    # Supondo um arquivo: 789123|BOLACHA|9.90
    config_txt_pipe = {
        "layout_type": "delimited",
        "delimiter": "|", 
        "has_header": False,
        "map": {
            "ean": 0,    # 1ª coluna
            "desc": 1,   # 2ª coluna
            "price": 2   # 3ª coluna
        }
    }

    # EXEMPLO 2: Lendo um TXT Posicional (Sem separador)
    # Supondo: 7891234567890BOLACHA RECHEADA    000990
    config_txt_fixo = {
        "layout_type": "fixed_width",
        "has_header": False,
        "map": {
            # (Posição Inicial, Quantidade de Caracteres)
            "ean": (0, 13),   
            "desc": (13, 20), 
            "price": (33, 6)
        }
    }

    converter = GenericConverter()
    
    # Teste: Mude aqui para o nome do seu arquivo real
    arquivo_entrada = "test.txt"
    arquivo_saida = "itens_para_vp.txt"
    
    # Usando a config de PIPE como exemplo
    qtd = converter.convert(arquivo_entrada, arquivo_saida, config_txt_pipe)
    
    if qtd > 0:
        print(f"✅ Sucesso! Gerado '{arquivo_saida}' com {qtd} produtos.")
        print("Agora é só usar o uploader para enviar!")
    else:
        print("⚠️ Nenhum produto convertido. Verifique o caminho do arquivo.")

if __name__ == "__main__":
    main()