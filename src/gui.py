import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.converter import GenericConverter

class PriceCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tanca/Jetway Importer Tool")
        self.root.geometry("600x550")
        
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Abas
        self.notebook = ttk.Notebook(root)
        self.tab_analyze = ttk.Frame(self.notebook)
        self.tab_convert = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_analyze, text="🔍 Analisar Erros")
        self.notebook.add(self.tab_convert, text="⚙️ Gerar Arquivo")
        self.notebook.pack(expand=True, fill='both')
        
        self._setup_analyze_tab()
        self._setup_convert_tab()

    def _setup_analyze_tab(self):
        frame = ttk.Frame(self.tab_analyze, padding=20)
        frame.pack(fill='both', expand=True)

        # Seleção de Arquivo
        lbl_info = ttk.Label(frame, text="Identifique produtos fora do padrão (sem preço, erro de layout, etc).", wraplength=550)
        lbl_info.pack(pady=(0, 10))

        file_frame = ttk.Frame(frame)
        file_frame.pack(fill='x', pady=5)
        
        self.entry_analyze_file = ttk.Entry(file_frame)
        self.entry_analyze_file.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        btn_browse = ttk.Button(file_frame, text="Selecionar Arquivo", command=lambda: self._select_file(self.entry_analyze_file))
        btn_browse.pack(side='right')

        # Configuração Básica (Delimitador)
        config_frame = ttk.LabelFrame(frame, text="Configuração Rápida", padding=10)
        config_frame.pack(fill='x', pady=10)
        
        ttk.Label(config_frame, text="Delimitador (se CSV/TXT):").grid(row=0, column=0, padx=5, sticky='w')
        self.entry_analyze_delim = ttk.Entry(config_frame, width=5)
        self.entry_analyze_delim.insert(0, "|")
        self.entry_analyze_delim.grid(row=0, column=1, sticky='w')

        # Botão Ação
        btn_run = ttk.Button(frame, text="Analisar Arquivo Agora", command=self._run_analysis)
        btn_run.pack(fill='x', pady=10)

        # Área de Resultado
        ttk.Label(frame, text="Relatório de Problemas:").pack(anchor='w')
        self.txt_log = scrolledtext.ScrolledText(frame, height=15)
        self.txt_log.pack(fill='both', expand=True)

    def _setup_convert_tab(self):
        frame = ttk.Frame(self.tab_convert, padding=20)
        frame.pack(fill='both', expand=True)

        # --- Arquivos ---
        grp_files = ttk.LabelFrame(frame, text="Arquivos", padding=10)
        grp_files.pack(fill='x', pady=5)

        ttk.Label(grp_files, text="Origem (Cliente):").grid(row=0, column=0, sticky='w')
        self.entry_src = ttk.Entry(grp_files)
        self.entry_src.grid(row=0, column=1, sticky='ew', padx=5)
        ttk.Button(grp_files, text="...", width=3, command=lambda: self._select_file(self.entry_src)).grid(row=0, column=2)

        ttk.Label(grp_files, text="Destino (VP):").grid(row=1, column=0, sticky='w')
        self.entry_dst = ttk.Entry(grp_files)
        self.entry_dst.insert(0, "itens.txt")
        self.entry_dst.grid(row=1, column=1, sticky='ew', padx=5)
        ttk.Button(grp_files, text="...", width=3, command=lambda: self._save_file(self.entry_dst)).grid(row=1, column=2)

        grp_files.columnconfigure(1, weight=1)

        # --- Tipo de Layout ---
        grp_layout = ttk.LabelFrame(frame, text="Tipo de Layout", padding=10)
        grp_layout.pack(fill='x', pady=10)

        self.var_layout = tk.StringVar(value="delimited")
        
        r1 = ttk.Radiobutton(grp_layout, text="Delimitado (CSV, Pipe |)", variable=self.var_layout, value="delimited", command=self._toggle_inputs)
        r2 = ttk.Radiobutton(grp_layout, text="Posicional (Largura Fixa)", variable=self.var_layout, value="fixed_width", command=self._toggle_inputs)
        r1.grid(row=0, column=0, padx=10)
        r2.grid(row=0, column=1, padx=10)

        # --- Mapeamento ---
        self.grp_map = ttk.LabelFrame(frame, text="Mapeamento das Colunas", padding=10)
        self.grp_map.pack(fill='x', pady=5)

        # Labels Dinâmicos
        self.lbl_help = ttk.Label(self.grp_map, text="Informe o número da coluna (começando em 0).", font=("Arial", 8, "italic"))
        self.lbl_help.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # EAN
        ttk.Label(self.grp_map, text="EAN (Barras):").grid(row=1, column=0, sticky='e')
        self.entry_ean = ttk.Entry(self.grp_map)
        self.entry_ean.grid(row=1, column=1, sticky='ew', padx=5, pady=2)
        
        # Descrição
        ttk.Label(self.grp_map, text="Descrição:").grid(row=2, column=0, sticky='e')
        self.entry_desc = ttk.Entry(self.grp_map)
        self.entry_desc.grid(row=2, column=1, sticky='ew', padx=5, pady=2)

        # Preço
        ttk.Label(self.grp_map, text="Preço:").grid(row=3, column=0, sticky='e')
        self.entry_price = ttk.Entry(self.grp_map)
        self.entry_price.grid(row=3, column=1, sticky='ew', padx=5, pady=2)

        # Extra (Só para delimitado)
        self.lbl_delim = ttk.Label(self.grp_map, text="Separador:")
        self.entry_delim = ttk.Entry(self.grp_map, width=5)
        self.entry_delim.insert(0, "|")
        
        # Posicionar inputs iniciais
        self._toggle_inputs()

        # Botão Converter
        btn_convert = ttk.Button(frame, text="FORMATAR E GERAR ARQUIVO", command=self._run_conversion)
        btn_convert.pack(fill='x', pady=20)

    def _toggle_inputs(self):
        mode = self.var_layout.get()
        if mode == 'delimited':
            self.lbl_help.config(text="Modo Delimitado: Informe o Nº da Coluna (0, 1, 2...).")
            self.lbl_delim.grid(row=4, column=0, sticky='e')
            self.entry_delim.grid(row=4, column=1, sticky='w', padx=5)
            # Defaults
            if not self.entry_ean.get(): self.entry_ean.insert(0, "0")
            if not self.entry_desc.get(): self.entry_desc.insert(0, "1")
            if not self.entry_price.get(): self.entry_price.insert(0, "2")

        else:
            self.lbl_help.config(text="Modo Fixo: Informe 'Inicio,Tamanho' (Ex: 0,13).")
            self.lbl_delim.grid_forget()
            self.entry_delim.grid_forget()
            # Defaults
            self.entry_ean.delete(0, tk.END); self.entry_ean.insert(0, "0,13")
            self.entry_desc.delete(0, tk.END); self.entry_desc.insert(0, "13,20")
            self.entry_price.delete(0, tk.END); self.entry_price.insert(0, "33,10")

    def _select_file(self, entry):
        path = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt *.csv"), ("Todos", "*.*")])
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

    def _save_file(self, entry):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivo Texto", "*.txt")])
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

    def _run_analysis(self):
        """Lógica simples para validar o arquivo sem converter"""
        path = self.entry_analyze_file.get()
        delim = self.entry_analyze_delim.get()
        
        if not os.path.exists(path):
            messagebox.showerror("Erro", "Arquivo não encontrado.")
            return

        self.txt_log.delete(1.0, tk.END)
        self.txt_log.insert(tk.END, f"Iniciando análise de: {path}\n\n")
        
        erros = 0
        linhas_ok = 0
        
        try:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                for i, line in enumerate(f):
                    line = line.strip()
                    if not line: continue
                    
                    parts = line.split(delim)
                    
                    # Validação 1: Quantidade de colunas
                    if len(parts) < 3:
                        self.txt_log.insert(tk.END, f"[Linha {i+1}] ERRO: Apenas {len(parts)} colunas encontradas (esperado min 3).\n", "error")
                        erros += 1
                        continue
                        
                    # Validação 2: Preço numérico?
                    possivel_preco = parts[-1] if parts[-1] else parts[-2]
                    clean_price = possivel_preco.replace('R$', '').replace('.', '').replace(',', '').strip()
                    
                    if not clean_price.isdigit():
                         self.txt_log.insert(tk.END, f"[Linha {i+1}] AVISO: Preço '{possivel_preco}' parece inválido.\n")
                         erros += 1
                    else:
                        linhas_ok += 1
            
            self.txt_log.insert(tk.END, f"\n--- Resumo ---\nLinhas OK: {linhas_ok}\nLinhas com Problemas: {erros}")
            self.txt_log.tag_config("error", foreground="red")

        except Exception as e:
            messagebox.showerror("Erro Crítico", str(e))

    def _run_conversion(self):
        source = self.entry_src.get()
        dest = self.entry_dst.get()
        layout = self.var_layout.get()
        
        if not source or not dest:
            messagebox.showwarning("Atenção", "Selecione arquivo de origem e destino.")
            return

        # Montar Configuração
        try:
            config = {
                "layout_type": layout,
                "has_header": False,
                "map": {}
            }

            if layout == 'delimited':
                config["delimiter"] = self.entry_delim.get()
                config["map"]["ean"] = int(self.entry_ean.get())
                config["map"]["desc"] = int(self.entry_desc.get())
                config["map"]["price"] = int(self.entry_price.get())
            else:
                # Parser de "Inicio,Tamanho" -> (Inicio, Tamanho)
                def parse_tuple(s):
                    parts = s.split(',')
                    return (int(parts[0]), int(parts[1]))
                
                config["map"]["ean"] = parse_tuple(self.entry_ean.get())
                config["map"]["desc"] = parse_tuple(self.entry_desc.get())
                config["map"]["price"] = parse_tuple(self.entry_price.get())

            # Chamar o Core
            converter = GenericConverter()
            qtd = converter.convert(source, dest, config)
            
            if qtd > 0:
                messagebox.showinfo("Sucesso", f"Arquivo gerado com sucesso!\n{qtd} produtos processados.\nSalvo em: {dest}")
            else:
                messagebox.showwarning("Aviso", "Nenhum produto foi gerado. Verifique o mapeamento.")

        except ValueError:
            messagebox.showerror("Erro", "Valores de mapeamento inválidos. Use números inteiros.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na conversão: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PriceCheckerApp(root)
    root.mainloop()