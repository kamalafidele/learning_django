from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def product_list(request: Request):
    if request.method == 'GET':
            query_set = Product.objects.select_related('collection').all()[:10]
            serializer = ProductSerializer(query_set, many=True)
            return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT'])
def product_details(request: Request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == 'GET':            
            serializer = ProductSerializer(product)
            return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)