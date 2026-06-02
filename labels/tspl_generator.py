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
        
        # Posições X das 3 colunas (aumentado para afastar da borda esquerda)
        xs = [35, 275, 515]
        
        for x in xs:
            # Nome do produto (Y=25), fonte 1 (menor)
            product_trunc = product_name[:22] # Limita caracteres para não vazar
            commands.append(f'TEXT {x},25,"1",0,1,1,"{product_trunc}"')
            
            # Código interno e Preço na mesma linha (Y=50)
            commands.append(f'TEXT {x},50,"1",0,1,1,"COD:{code}"')
            commands.append(f'TEXT {x + 100},50,"1",0,1,1,"{price_display}"')
            
            # Código de barras baixo (Y=75), altura 30 dots
            # Usando proporção 1,1 para ficar mais estreito e caber
            if barcode:
                commands.append(f'BARCODE {x},75,"128",30,0,0,1,1,"{barcode}"')
                commands.append(f'TEXT {x},110,"1",0,1,1,"{barcode}"')
                
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
