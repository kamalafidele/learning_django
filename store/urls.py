from django.urls import path
from . import views


urlpatterns = [
   path('products/', views.ProductList.as_view()),
   path('products/<int:id>/', views.ProductDetails.as_view()),
   path('collections/', views.CollectionList.as_view()),
   path('collections/<int:id>/', views.CollectionDetails.as_view())
]
