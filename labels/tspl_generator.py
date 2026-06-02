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
            'DIRECTION 0',
            'CLS',
        ]
        
        # Posições X das 3 colunas (margem + 240 dots por coluna)
        xs = [10, 250, 490]
        
        for x in xs:
            # Nome do produto reduzido (Y=10)
            product_trunc = product_name[:20] # Evita invadir a próxima coluna
            commands.append(f'TEXT {x},10,"2",0,1,1,"{product_trunc}"')
            
            # Código interno (Y=40)
            commands.append(f'TEXT {x},40,"1",0,1,1,"COD: {code}"')
            
            # Preço em destaque (Y=40, mais à direita)
            commands.append(f'TEXT {x + 100},40,"2",0,1,1,"{price_display}"')
            
            # Código de barras baixo (Y=70)
            # Altura 30 dots, texto invisível (0)
            if barcode:
                commands.append(f'BARCODE {x},70,"128",30,0,0,2,2,"{barcode}"')
                commands.append(f'TEXT {x},105,"1",0,1,1,"{barcode}"')
                
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
