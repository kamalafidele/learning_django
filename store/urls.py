from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls import include
from rest_framework_nested import routers


# router = DefaultRouter()
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet, basename='carts')
router.register('customers', views.CustomerViewSet)

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = [
   path('', include(router.urls)),
   path('', include(product_router.urls)),
   path('', include(carts_router.urls)),
   # path('products/', views.ProductViewSet.as_view()),
   # path('collections/<int:pk>/', views.CollectionViewSet.as_view())
]
