from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls import include


router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)


urlpatterns = [
   path('', include(router.urls))
   # path('products/', views.ProductViewSet.as_view()),
   # path('collections/<int:pk>/', views.CollectionViewSet.as_view())
]
