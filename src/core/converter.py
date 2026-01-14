import csv
import re
from typing import Dict
from src.core.formatter import VPFormatter

class GenericConverter:
    def __init__(self):
        self.formatter = VPFormatter()

    def convert(self, source_path: str, output_path: str, config: Dict):
        lines_converted = []
        layout_type = config.get('layout_type', 'delimited')
        try:
            with open(source_path, 'r', encoding='utf-8', errors='replace') as f:
                if layout_type == 'delimited':
                    delimiter = config.get('delimiter', ';')
                    reader = csv.reader(f, delimiter=delimiter)
                    for i, row in enumerate(reader):
                        if config.get('has_header') and i == 0: continue
                        if not row: continue
                        try:
                            raw_ean = row[config['map']['ean']]
                            raw_desc = row[config['map']['desc']]
                            raw_price = row[config['map']['price']]
                            vp_line = self._process_data(raw_ean, raw_desc, raw_price)
                            lines_converted.append(vp_line)
                        except IndexError:
                            pass 
                elif layout_type == 'fixed_width':
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        if config.get('has_header') and i == 0: continue
                        if not line.strip(): continue
                        try:
                            mapa = config['map']
                            def get_chunk(start, length):
                                if start + length > len(line): return ""
                                return line[start : start+length].strip()
                            raw_ean = get_chunk(mapa['ean'][0], mapa['ean'][1])
                            raw_desc = get_chunk(mapa['desc'][0], mapa['desc'][1])
                            raw_price = get_chunk(mapa['price'][0], mapa['price'][1])
                            vp_line = self._process_data(raw_ean, raw_desc, raw_price)
                            lines_converted.append(vp_line)
                        except Exception as e:
                            print(f"Erro linha {i}: {e}")
            with open(output_path, 'w', encoding='latin-1', newline='\r\n') as f_out:
                f_out.write("\n".join(lines_converted))
            return len(lines_converted)
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {source_path}")
            return 0

    def _process_data(self, ean, desc, price_raw):
        clean_price = self._sanitize_price(price_raw)
        return self.formatter.process_line(ean, desc, clean_price)

    def _sanitize_price(self, price_str: str) -> float:
        if not price_str: return 0.0
        
        clean = price_str.replace('R$', '').strip()
        
        try:
            if ',' in clean:
                if '.' in clean:
                    clean = clean.replace('.', '')
                clean = clean.replace(',', '.')
            return float(clean)
        except ValueError:
            print(f"Aviso: Preço inválido encontrado: '{price_str}'. Será zerado.")
            return 0.0