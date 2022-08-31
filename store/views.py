from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
from .models import Collection, Product
from .serializers import ProductSerializer, CollectionSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


# Create your views here.

class ProductList(ListCreateAPIView):
        queryset = Product.objects.select_related('collection').all()
        serializer_class = ProductSerializer
        
        def get_serializer_context(self):
                return {'request': self.request }


class ProductDetails(RetrieveUpdateDestroyAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer

        def get_serializer_context(self):
                return {'request': self.request }
        
        # HERE I CUSTOMIZED THE DELETE METHOD SO THAT I CAN ADD MY EXTRA LOGIC
        def delete(self, request, id):
                product = get_object_or_404(Product, pk=id)
                if product.orderitem_set.count() > 0:
                        errorMessage = 'Product cannot be delete since it associated with orders'
                        return Response({ 'error': errorMessage },status=status.HTTP_405_METHOD_NOT_ALLOWED)
                product.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
        queryset = Collection.objects.annotate(products_count=Count('products')).all()
        serializer_class = CollectionSerializer

        def get_serializer_context(self):
                return {'request': self.request }
                
                
class CollectionDetails(RetrieveUpdateDestroyAPIView):
        queryset = Collection.objects.annotate(products_count=Count('products'))
        serializer_class = CollectionSerializer

        def delete(self, request, pk):
                collection: Collection = get_object_or_404(Collection, pk=pk)
                if collection.products.count() > 0:
                        return Response({'error': 'Collection cannot be deleted, it is associated with products'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                collection.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)