from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
# from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from .filters import ProductFilter
from .models import Cart, Collection, OrderItem, Product, Review
from .serializers import CartSerializer, ProductSerializer, CollectionSerializer, ReviewSerializer

class ProductViewSet(ModelViewSet):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer

        # GENERIC FILTERING
        filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
        # filterset_fields = ['collection_id']
        filterset_class = ProductFilter
        pagination_class = PageNumberPagination

        search_fields = ['title', 'description']
        ordering_fields = ['unit_price', 'last_update']

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
        pagination_class = PageNumberPagination
        filter_backends = [SearchFilter]
        search_fields = ['title']

        def destroy(self, request, *args, **kwargs):
                if Collection.objects.filter(pk=kwargs['pk']).get().products.count() > 0:
                        return Response({'error': 'Collection cannot be deleted, it is associated with products'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
        # queryset = Review.objects.all()
        serializer_class = ReviewSerializer

        def get_queryset(self):
                return Review.objects.filter(product_id=self.kwargs['product_pk'])

        def get_serializer_context(self):
                return { 'product_id': self.kwargs['product_pk'] }


class CartViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
        # queryset = Cart.objects.prefetch_related('items__product').all()
        queryset = Cart.objects.all()
        serializer_class = CartSerializer
