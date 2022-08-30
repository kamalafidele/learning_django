from django.http import HttpResponse
from store.models import Customer
from store.models import Product
from django.db.models import Q, F, Min, Max, Count, Avg, Value
from django.db.models.functions import Concat
from django.shortcuts import render


# Create your views here.
def say_hello(request):
    return HttpResponse("Hello, you got me!!!")

    #  query_set = Customer.objects.filter(first_name__icontains="Kamara")
    #  other = Customer.objects.filter(first_name__startswith="M")
    #  products = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    #  customers = list(query_set)
     
    #  # Complex filtering
    #  query_set_2 = Product.objects.filter(inventory__gt=10).filter(unit_price__lt=20)
    #  query_set_3 = Product.objects.filter(Q(inventory__gt=10) | Q(unit_price__lt=20))
    #  # Filtering objects on equality of the fields
    #  query_set_4 = Product.objects.filter(inventory=F('unit_price'))

    #  # Sorting objects from the database
    #  query_set_5 = Product.objects.order_by('title')

    #  # Limiting the results
    #  query_set_6 = Product.objects.all()[:5]

    #  # Projection ( Selecting specific attributes )
    #  query_set_7 = Product.objects.values('id','title','collection__title')
     
    #  # SELECTING RELATED OBJECTS
    #  query_set_8 = Product.objects.select_related('collection').all()

    #  # Aggregating
    #  result = Customer.objects.aggregate(count=Count('id'))
   

    #  # Database functions
    #  query_set_9 =  Product.objects.annotate(full_name=Concat('first_name',Value(' '),'last_name'))

    #  print(Customer.objects.all())

    #  return query_set_7