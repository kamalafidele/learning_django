from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
from .models import Collection, OrderItem, Product
from .serializers import ProductSerializer, CollectionSerializer
from rest_framework.viewsets import ModelViewSet
# from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView

class ProductViewSet(ModelViewSet):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer

        # HERE I CUSTOMIZED THE DESTROY METHOD SO THAT I CAN ADD MY EXTRA LOGIC
        def destroy(self, request, *args, **kwargs):
                if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
                        errorMessage = 'Product cannot be delete since it associated with orders'
                        return Response({ 'error': errorMessage },status=status.HTTP_405_METHOD_NOT_ALLOWED)
                
                return super().destroy(request, *args, **kwargs)

        def get_serializer_context(self):
                return {'request': self.request }


class CollectionViewSet(ModelViewSet):
        queryset = Collection.objects.annotate(products_count=Count('products')).all()
        serializer_class = CollectionSerializer

        def destroy(self, request, *args, **kwargs):
                if Collection.objects.filter(pk=kwargs['pk']).get().products.count() > 0:
                        return Response({'error': 'Collection cannot be deleted, it is associated with products'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                return super().destroy(request, *args, **kwargs)

        def get_serializer_context(self):
                return {'request': self.request }