from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .tspl_generator import generate_tspl
import base64
import os
from django.conf import settings
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization


@api_view(['POST'])
def generate_tspl_view(request):
    data = request.data
    
    # Validação simples
    required_fields = ['product_name', 'code', 'price']
    for field in required_fields:
        if field not in data:
            return Response(
                {'error': f'O campo {field} é obrigatório'}, 
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
        with open(key_path, 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
        
        signature = private_key.sign(
            message.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA512()
        )
        
        return Response(base64.b64encode(signature).decode('utf-8'), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
