import textwrap

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

    model = data.get('model', 'large')

    # Formata preço
    price_display = f"R$ {price}"

    if model == 'small_3':
        # Etiqueta Argox 90x15 (3 colunas)
        # Largura total 90mm (720 dots), Altura 15mm (120 dots)
        # Colunas com largura aprox de 30mm (240 dots)
        commands = [
            'SIZE 90 mm, 15 mm',
            'GAP 3 mm, 0 mm',
            'DIRECTION 1',  # Invertido para sair de cabeça para cima
            'CLS',
        ]
        
        # Posições X das 3 colunas (reduzido para ir um pouco mais para a esquerda)
        xs = [20, 260, 500]
        
        for x in xs:
            # Nome do produto com quebra de linha inteligente (máx 22 chars, 2 linhas)
            wrapped_name = textwrap.wrap(product_name, width=22)[:2]
            
            y_offset = 10
            for line in wrapped_name:
                commands.append(f'TEXT {x},{y_offset},"1",0,1,1,"{line}"')
                y_offset += 15
            
            # Código interno e Preço (Y=45 para caber embaixo das 2 linhas de texto)
            commands.append(f'TEXT {x},45,"1",0,1,1,"COD:{code}"')
            commands.append(f'TEXT {x + 100},45,"1",0,1,1,"{price_display}"')
            
            # Código de barras (Y=65), altura 30 dots
            if barcode:
                commands.append(f'BARCODE {x},65,"128",30,0,0,1,1,"{barcode}"')
                commands.append(f'TEXT {x},100,"1",0,1,1,"{barcode}"')
                
        commands.append(f'PRINT {copies},1')

    elif model == 'medium_115x35':
        # Etiqueta Argox 115x35 (1 coluna larga)
        # Largura total 115mm (920 dots), Altura 35mm (280 dots)
        commands = [
            'SIZE 115 mm, 35 mm',
            'GAP 3 mm, 0 mm',
            'DIRECTION 1',
            'CLS',
        ]
        
        # Nome do produto (Y=20)
        # Como é larga, podemos usar fonte 2 ou 3 e não precisa quebrar linha logo cedo
        product_trunc = product_name[:45]
        commands.append(f'TEXT 30,20,"2",0,1,1,"{product_trunc}"')
        
        # Código interno (Y=70)
        commands.append(f'TEXT 30,70,"2",0,1,1,"COD: {code}"')
        
        # Código de barras (Y=120) - bem grande
        if barcode:
            commands.append(f'BARCODE 30,120,"128",80,1,0,2,2,"{barcode}"')
            
        # Preço em destaque à direita (Y=120)
        commands.append(f'TEXT 550,120,"4",0,1,1,"{price_display}"')
        
        commands.append(f'PRINT {copies},1')
    
    else:
        # Etiqueta Padrão Grande (100x60mm)
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
            f'BARCODE 10,80,"128",60,1,0,2,2,"{barcode}"',

            # Preço — destaque à direita, fonte maior
            f'TEXT 320,80,"4",0,1,1,"{price_display}"',

            # Imprime X cópias
            f'PRINT {copies},1',
        ]

    return '\r\n'.join(commands) + '\r\n'
