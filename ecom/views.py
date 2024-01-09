from django.shortcuts import render,redirect,get_object_or_404
from . import models
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse

def home_view(request):
    products=models.Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    return render(request,'ecom/index.html',{'products':products,'product_count_in_cart':product_count_in_cart})

def logouthandle(request):
    logout(request)
    return redirect('/')

def user_not_authenticated(user):
    return not user.is_authenticated

@user_passes_test(user_not_authenticated, login_url='/')
def handlelogin(request):
    if request.method=="POST":
        loginemail=request.POST['email'].lower()
        loginpassword=request.POST['password']
        user=authenticate(username=loginemail, password= loginpassword)
        print(loginemail,loginpassword)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Please Try Again")
            return render(request, 'ecom/signin.html')
        
    else:
        return render(request, 'ecom/signin.html')

def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        fname = request.POST['name']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        username = email

        if User.objects.filter(email=email).exists():
            messages.error(request, "User with this Email already exists")
            return redirect('/signup') 
        try:
            validate_password(pass1, user=User)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect('/signup')  
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('/signup')  
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.save()

        messages.success(request, "Account created successfully")
        return redirect('/signin')  # Adjust the URL for the home page

    return render(request, 'ecom/signup.html')

# admin view the product
@login_required(login_url='admin')
def admin_products_view(request):
    products=models.Product.objects.all()
    return render(request,'ecom/admin_products.html',{'products':products})

@login_required(login_url='admin')
def delete_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    product.delete()
    return redirect('admin-products')

def order(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        gender = request.POST['gender']
        service = request.POST['service']
        address = request.POST['address']  # Add this line to capture the address
        notes = request.POST['Ordernotes']  # Make sure the name matches your HTML form

        # Create an instance of the Orders model and save it to the database
        order_instance = models.ServiceOrders(name=name, email=email, phone=phone, gender=gender, service=service, address=address, notes=notes)
        order_instance.save()

        return render(request, 'ecom/ordersuccess.html')
    
    return render(request, 'ecom/placeorder.html')



def add_to_cart_view(request, pk):
    response_data={}
    if not request.user.is_authenticated:
        return redirect('/signin')
    try:
        product = get_object_or_404(models.Product, id=pk)
    except models.Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    # Check if the item is already in the cart
    if models.CartItem.objects.filter(user=request.user, product=product).exists():
        return JsonResponse({'message': 'Product already in the cart'})
    else:
         models.CartItem.objects.create(user=request.user, product=product)

         response_data = {
             'message': f'{product.name} added to cart successfully!',
         }

    return JsonResponse(response_data)

@login_required
def cart_view(request):
   # Retrieve the CartItem objects for the current user
    cart_items = models.CartItem.objects.filter(user=request.user)

    # Get the product IDs from CartItem objects
    product_ids = [item.product_id for item in cart_items]

    # Retrieve the actual Product objects corresponding to the product IDs
    products = models.Product.objects.filter(id__in=product_ids)

    # Calculate the total price
    total = sum(item.product.price for item in cart_items)

    # Count the number of items in the cart
    cart_item_count = cart_items.count()

    return render(request, 'ecom/cart.html', {'cart_items': cart_items, 'products': products, 'total': total, 'cart_item_count': cart_item_count})

def remove_from_cart_view(request,pk):
    cart_item = get_object_or_404(models.CartItem, user=request.user, product_id=pk)

    cart_item.delete()

    total = sum(item.product.price for item in models.CartItem.objects.filter(user=request.user))

    cart_item_count = models.CartItem.objects.filter(user=request.user).count()
  # Get the product IDs from CartItem objects
    cart_items = models.CartItem.objects.filter(user=request.user)
    product_ids = [item.product_id for item in cart_items]

    # Retrieve the actual Product objects corresponding to the product IDs
    products = models.Product.objects.filter(id__in=product_ids)

    return render(request, 'ecom/cart.html', {'products': products,'total': total, 'cart_item_count': cart_item_count})

def checkout(request):

    
    cart_item_count = request.GET.get('cart_item_count')
    cart_items= models.CartItem.objects.filter(user=request.user)
    
    # Get the product IDs from CartItem objects
    product_ids = [item.product_id for item in cart_items]

    # Retrieve the actual Product objects corresponding to the product IDs
    products = models.Product.objects.filter(id__in=product_ids)
    total = sum(item.product.price for item in cart_items)
    product_names =  set(item.product.name for item in cart_items)
   
    if request.method=="POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        product_names_str = ', '.join(product_names)
        order = models.Orders(firstname=firstname,lastname=lastname,email=email,phone=phone,address=address,total=total,products=product_names_str)
        order.save()
        cart_items.delete()
        return render(request,'ecom/ordersuccess.html')
    
    context={"cart_item_count":cart_item_count,"products":products,"total":total}
    return render(request, 'ecom/checkout.html',context)

def productdetails(request,pk):
    product= models.Product.objects.filter(id=pk).first()
    return render(request, 'ecom/productdetails.html', {"product" : product})


def search_view(request):
    query = request.GET.get('searchinput', '') 
    productsq = models.Product.objects.filter(name__icontains=query)

    context = {'productsq': productsq, 'query': query}
    return render(request, 'ecom/products.html', context)

def product(request):
    products = models.Product.objects.all()
    return render(request,"ecom/products.html",{"products": products})

def aboutus_view(request):
    return render(request,'ecom/aboutus.html')

def contactus_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        msg = models.Contact(name=name, email=email,message=message)
        msg.save()
        return render(request, 'ecom/contactussuccess.html')
    
    return render(request, 'ecom/contactus.html')


def privacypolicy(request):
    return render(request,"ecom/privacypolicy.html")

def returnpolicy(request):
    return render(request,"ecom/returnpolicy.html")