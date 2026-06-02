def generate_tspl(data: dict) -> str:
    """
    Gera os comandos TSPL2 para a Bematech LB-1000.
    Etiqueta: 100mm x 60mm
    """
    product_name = data.get('product_name', '')
    code = data.get('code', '')
    barcode = data.get('barcode', '')
    price = data.get('price', '')
    copies = int(data.get('copies', 1))

    # Formata preço
    price_display = f"R$ {price}"

    commands = [
        'SIZE 100 mm, 60 mm',
        'GAP 3 mm, 0 mm',
        'DIRECTION 0',
        'CLS',

        # Nome do produto — topo, fonte grande, negrito
        f'TEXT 80,10,"3",0,1,1,"{product_name}"',

        # Código interno
        f'TEXT 80,50,"2",0,1,1,"COD: {code}"',

        # Código de barras EAN-13 (ou Code 128 se não for EAN)
        # Parâmetros: x, y, tipo, altura, legível, rotação, estreito, largo, dados
        f'BARCODE 10,80,"128",60,1,0,2,2,"{barcode}"',

        # Preço — destaque à direita, fonte maior
        f'TEXT 320,80,"4",0,1,1,"{price_display}"',

        # Linha separadora opcional
        # 'LINE 300,10,300,190,2',

        # Imprime X cópias
        f'PRINT {copies},1',
    ]

    return '\r\n'.join(commands) + '\r\n'
