import textwrap
import os
from io import BytesIO
try:
    from PIL import Image
except ImportError:
    Image = None

def generate_logo_bitmap(x, y):
    logo_path = os.path.join(os.path.dirname(__file__), 'image.png')
    if not os.path.exists(logo_path) or not Image:
        return b""
        
    img = Image.open(logo_path).convert('1')
    img.thumbnail((120, 120)) # Reduced max size to 120x120 to leave bottom margin
    width, height = img.size
    
    width_bytes = (width + 7) // 8
    bitmap_data = bytearray()
    
    for py in range(height):
        for px in range(width_bytes):
            byte = 0
            for bit in range(8):
                ix = px * 8 + bit
                if ix < width:
                    # In PIL '1' mode, 0 is black, 255 is white
                    pixel = img.getpixel((ix, py))
                    if pixel == 0:
                        byte |= (1 << (7 - bit))
            bitmap_data.append(byte)
            
    header = f'BITMAP {x},{y},{width_bytes},{height},0,'.encode('ascii')
    return header + bytes(bitmap_data) + b'\r\n'

def generate_tspl(data: dict) -> any:
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
            'GAP 2 mm, 0 mm',
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
        return '\r\n'.join(commands) + '\r\n'

    elif model == 'medium_115x35':
        # Etiqueta Argox 115x35 (1 coluna larga com Logo)
        # Largura total 115mm (920 dots), Altura 35mm (280 dots)
        commands1 = [
            'SIZE 115 mm, 35 mm',
            'GAP 3 mm, 0 mm',
            'DIRECTION 1',
            'CLS',
        ]
        
        # Nome do produto no topo (Y=40 para dar margem superior)
        product_trunc = product_name[:35] # Limita a 35 chars para não encostar na borda direita
        commands1.append(f'TEXT 60,40,"3",0,1,1,"{product_trunc}"')
        
        tspl_str1 = '\r\n'.join(commands1) + '\r\n'
        
        # O resto dos comandos
        commands2 = []
        commands2.append(f'TEXT 300,120,"2",0,1,1,"COD: {code}"')
        
        if barcode:
            # Altura 60 em vez de 80 para dar margem inferior
            commands2.append(f'BARCODE 300,160,"128",60,1,0,2,2,"{barcode}"')
            
        # Preço (X=580 para deixar margem direita)
        commands2.append(f'TEXT 580,160,"4",0,1,1,"{price_display}"')
        commands2.append(f'PRINT {copies},1')
        
        tspl_str2 = '\r\n'.join(commands2) + '\r\n'
        
        # Cria array de bytes completo para enviar como HEX e evitar corrupção de charset
        raw_bytes = bytearray()
        raw_bytes.extend(tspl_str1.encode('iso-8859-1'))
        raw_bytes.extend(generate_logo_bitmap(60, 110)) # Logo X=60, Y=110
        raw_bytes.extend(tspl_str2.encode('iso-8859-1'))
        
        return [{
            "type": "raw",
            "format": "hex",
            "data": raw_bytes.hex()
        }]
    
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
