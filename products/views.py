from django.shortcuts import render,HttpResponse
from .models import ClothProduct

def allproducts(request):
    return render(request, 'products/products.html')  

def productdetails(request):
    return render(request, 'products/productdetails.html') 

def checkout(request):
    return render(request, 'products/checkout.html') 


def cart(request):
    return render(request,"products/cart.html")

def search(request):
    query=request.GET['query']
    if len(query)>78:
        allPosts=ClothProduct.objects.none()
    else:
        allPostsTitle= ClothProduct.objects.filter(title__icontains=query)
        allPostsAuthor= ClothProduct.objects.filter(author__icontains=query)
        allPostsContent =ClothProduct.objects.filter(content__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor)
    if allPosts.count()==0:
        return HttpResponse("Hello There")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)