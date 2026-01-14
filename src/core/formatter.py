import unicodedata

class VPFormatter:
    def __init__(self):
        self.EAN_LEN = 13
        self.DESC_LEN = 20
        self.PRICE_TOTAL_LEN = 20
        self.PRICE_DIGITS_LEN = 10
        self.SEPARATOR = "|"
    
    def remove_accents(self, text: str) -> str:
        if not text:
            return ""
        nfkd_form = unicodedata.normalize('NFKD', text)
        only_ascii = nfkd_form.encode('ASCII', 'ignore').decode('utf-8')
        return only_ascii.upper()

    def format_price(self, price: float) -> str:
        cents = int(round(price * 100))
        price_str = f"{cents:0{self.PRICE_DIGITS_LEN}d}"
        padding = " " * (self.PRICE_TOTAL_LEN - self.PRICE_DIGITS_LEN)
        
        return f"{padding}{price_str}"

    def process_line(self, ean: str, description: str, price: float) -> str:
        ean_clean = str(ean).strip() if ean else ""
        ean_fmt = ean_clean.zfill(self.EAN_LEN)[:self.EAN_LEN]

        desc_clean = self.remove_accents(description)
        desc_fmt = desc_clean[:self.DESC_LEN].ljust(self.DESC_LEN)
        price_fmt = self.format_price(price)
        return f"{ean_fmt}{self.SEPARATOR}{desc_fmt}{self.SEPARATOR}{price_fmt}"

# --- EXEMPLO DE USO (Teste Rápido) ---
if __name__ == "__main__":
    converter = VPFormatter()

    produtos_teste = [
        {"ean": "7898141260048", "desc": "Biscoito Sempre Azed", "preco": 9.99},
        {"ean": "789123456", "desc": "Pão de Alho c/ Queijo Extra", "preco": 25.50},
        {"ean": "123", "desc": "Água", "preco": 1.99},
    ]

    print("--- SIMULAÇÃO DO ARQUIVO GERADO ---")
    lines = []
    for p in produtos_teste:
        linha = converter.process_line(p["ean"], p["desc"], p["preco"])
        lines.append(linha)
        print(linha)

    with open("exportacao_vp.txt", "w", encoding="latin-1", newline='\r\n') as f:
        f.write("\n".join(lines))