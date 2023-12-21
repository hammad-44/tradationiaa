from django.shortcuts import render,HttpResponse

# Create your views here.
def allproducts(request):
    return HttpResponse("All Products")