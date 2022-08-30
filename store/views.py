from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import Collection, Product
from .serializers import ProductSerializer, CollectionSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def product_list(request: Request):
    if request.method == 'GET':
            query_set = Product.objects.select_related('collection').all()
            serializer = ProductSerializer(query_set, many=True)
            return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
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
    elif request.method == 'DELETE':
        if product.orderitem_set.count() > 0:
                errorMessage = 'Product cannot be delete since it associated with orders'
                return Response({ 'error': errorMessage },status=status.HTTP_405_METHOD_NOT_ALLOWED)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def collection_list(request: Request):
        if request.method == 'GET':
                collections = Collection.objects.all()
                serializer = CollectionSerializer(collections, many=True)
                return Response(serializer.data)
        elif request.method == 'POST':
                serializer = CollectionSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT','DELETE'])
def collection_details(request: Request, id):
        collection = get_object_or_404(Collection, pk=id)
        if request.method == 'GET':
                serializer = CollectionSerializer(collection)
                return Response(serializer.data)
        elif request.method == 'PUT':
                serializer = CollectionSerializer(collection, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
                collection.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)