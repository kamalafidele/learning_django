from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import Collection, Product
from .serializers import ProductSerializer, CollectionSerializer
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

# Create your views here.

class ProductList(APIView):
        def get(self, request):
            query_set = Product.objects.select_related('collection').all()
            serializer = ProductSerializer(query_set, many=True)
            return Response(serializer.data)

        def post(self, request):
                serializer = ProductSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
        
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetails(APIView):
        def get(self, request, id):
                product = get_object_or_404(Product, pk=id)
                serializer = ProductSerializer(product)
                return Response(serializer.data)

        def put(self, request, id):
                product = get_object_or_404(Product, pk=id)
                serializer = ProductSerializer(product,data=request.data)
                serializer.is_valid(raise_exception=True)
                
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        def delete(self, request, id):
                product = get_object_or_404(Product, pk=id)
                if product.orderitem_set.count() > 0:
                        errorMessage = 'Product cannot be delete since it associated with orders'
                        return Response({ 'error': errorMessage },status=status.HTTP_405_METHOD_NOT_ALLOWED)
                product.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(APIView):
        def get(self, request):
                collections = Collection.objects.all()
                serializer = CollectionSerializer(collections, many=True)
                return Response(serializer.data)
        
        def post(self, request):
                serializer = CollectionSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                

class CollectionDetails(APIView):
        def get(self, request, id):
                collection = get_object_or_404(Collection, pk=id)
                serializer = CollectionSerializer(collection)
                return Response(serializer.data)
        
        def put(self, request, id):
                collection = get_object_or_404(Collection, pk=id)
                serializer = CollectionSerializer(collection, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        def delete(self, request, id):
                collection = get_object_or_404(Collection, pk=id)
                collection.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)