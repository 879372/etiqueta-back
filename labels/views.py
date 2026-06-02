from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .tspl_generator import generate_tspl
import base64
import os
from django.conf import settings
from OpenSSL import crypto


@api_view(['POST'])
def generate_tspl_view(request):
    """
    Recebe os dados da etiqueta e retorna o TSPL2 gerado.
    """
    data = request.data

    # Validação mínima
    required = ['product_name', 'barcode', 'price']
    for field in required:
        if not data.get(field):
            return Response(
                {'error': f'Campo obrigatório ausente: {field}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    tspl = generate_tspl(data)
    return Response({'tspl': tspl}, status=status.HTTP_200_OK)

@api_view(['GET'])
def sign_qz(request):
    """
    Assina digitalmente a requisição do QZ Tray para remover a janela de aviso.
    """
    message = request.GET.get('request')
    if not message:
        return Response({'error': 'No request provided'}, status=400)
    
    try:
        key_path = os.path.join(settings.BASE_DIR, 'private-key.pem')
        with open(key_path, 'r') as key_file:
            key_data = key_file.read()
        
        pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, key_data)
        sign = crypto.sign(pkey, message.encode('utf-8'), 'sha512')
        
        return Response(base64.b64encode(sign).decode('utf-8'), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
