```txt
price-checker-importer/
│
├── src/
│   ├── __init__.py
│   ├── main.py             # Ponto de entrada (CLI ou GUI)
│   ├── core/
│   │   ├── parser.py       # Lógica de ler CSV/Excel/SQL
│   │   ├── formatter.py    # Lógica para formatar para Tanca/Jetway
│   │   └── uploader.py     # Lógica de envio (FTP/Socket/Copy)
│   ├── models/
│   │   └── product.py      # Dataclass do Produto (Nome, Preço, EAN)
│   └── utils/
│       └── text_utils.py   # Função para remover acentos/truncar texto
│
├── config/
│   └── settings.yaml       # Configurações (IP dos aparelhos, caminhos)
│
├── tests/                  # Testes unitários (Essencial para parsers!)
├── docs/                   # Documentação dos formatos Tanca/Jetway
├── requirements.txt
└── README.md
```