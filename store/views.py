from urllib import request
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from store.permissions import IsAdminOrReadOnly
# from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from .filters import ProductFilter
from .models import Cart, CartItem, Collection, Customer, Order, OrderItem, Product, Review
from .serializers import AddCartItemSeriliazer, CartSerializer, CustomerSerializer, OrderSerializer, ProductSerializer, CollectionSerializer, ReviewSerializer, CartItemSerializer, UpdateCartItemSerializer

class ProductViewSet(ModelViewSet):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        
        permission_classes = [IsAdminOrReadOnly]

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
        permission_classes = [IsAuthenticated]
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


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
        # queryset = Cart.objects.prefetch_related('items__product').all()
        queryset = Cart.objects.all()
        serializer_class = CartSerializer
        permission_classes = [IsAuthenticated]

class CartItemViewSet(ModelViewSet):
        queryset =  CartItem.objects.all()
        http_method_names: list[str] = ['get', 'post', 'patch']

        def get_serializer_class(self):
                if self.request.method == 'POST':
                        return AddCartItemSeriliazer
                elif self.request.method == 'PATCH':
                        return UpdateCartItemSerializer

                return CartItemSerializer

        def get_queryset(self):
                return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')

        def get_serializer_context(self):
                return { 'cart_id': self.kwargs['cart_pk'] }


class CustomerViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
        queryset = Customer.objects.all()
        serializer_class = CustomerSerializer
        permission_classes = [IsAuthenticated]

        # SETTING PERMISSIONS FOR ONLY CERTAIN ENDPOINTS
        def get_permissions(self):
                if self.request.method == 'GET':
                        return [AllowAny()]
                return [IsAuthenticated()]


        @action(detail=False, methods=['GET', 'PUT'])
        def me(self, request):
                customer = Customer.objects.get(user_id=request.user.id)
                if request.method == 'GET': 
                        serializer = CustomerSerializer(customer)
                        return Response(serializer.data)
                elif request.method == 'PUT':
                        serializer = CustomerSerializer(customer, data=request.data)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                        return Response(serializer.data)

class OrderViewSet(ModelViewSet):
        serializer_class = OrderSerializer
        filter_backends = [ DjangoFilterBackend ,SearchFilter, OrderingFilter]
        filterset_fields = ['customer']
        ordering_fields = ['placed_at']

        def get_permissions(self):
                if self.request.method in ['PUT', 'PATCH', 'DELETE']:
                        return [IsAdminUser()]
                return [IsAuthenticated()]

        def get_queryset(self):
                user = self.request.user
                if user.is_staff:
                        return Order.objects.all()
                customer_id = Customer.objects.only('id').get(user_id=user.id)
                return Order.objects.filter(customer_id=customer_id).all()
                
                        
