from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .tspl_generator import generate_tspl


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
    return Response({'tspl': tspl})
