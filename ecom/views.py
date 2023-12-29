from django.shortcuts import render,redirect
from . import models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User 
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


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


#---------------------------------------------------------------------------------
#------------------------ PUBLIC CUSTOMER RELATED VIEWS START ---------------------
#---------------------------------------------------------------------------------
def search_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    products=models.Product.objects.all().filter(name__icontains=query)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Searched Result :"

    if request.user.is_authenticated:
        return render(request,'ecom/customer_home.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})
    return render(request,'ecom/index.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})


# any one can add product to cart, no need of signin
def add_to_cart_view(request,pk):
    products=models.Product.objects.all()

    #for cart counter, fetching products ids added by customer from cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=1

    response = render(request, 'ecom/index.html',{'products':products,'product_count_in_cart':product_count_in_cart})

    #adding product id to cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids=="":
            product_ids=str(pk)
        else:
            product_ids=product_ids+"|"+str(pk)
        response.set_cookie('product_ids', product_ids)
    else:
        response.set_cookie('product_ids', pk)

    product=models.Product.objects.get(id=pk)
    messages.info(request, product.name + ' added to cart successfully!')
    return response



# for checkout of cart
def cart_view(request):
    #for cart counter
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # fetching product details from db whose id is present in cookie
    products=None
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart=product_ids.split('|')
            products=models.Product.objects.all().filter(id__in = product_id_in_cart)

            #for total price shown in cart
            for p in products:
                total=total+p.price
    return render(request,'ecom/cart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart})


def remove_from_cart_view(request,pk):
    #for counter in cart
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # removing product id from cookie
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        product_id_in_cart=product_ids.split('|')
        product_id_in_cart=list(set(product_id_in_cart))
        product_id_in_cart.remove(str(pk))
        products=models.Product.objects.all().filter(id__in = product_id_in_cart)
        #for total price shown in cart after removing product
        for p in products:
            total=total+p.price

        #  for update coookie value after removing product id in cart
        value=""
        for i in range(len(product_id_in_cart)):
            if i==0:
                value=value+product_id_in_cart[0]
            else:
                value=value+"|"+product_id_in_cart[i]
        response = render(request, 'ecom/cart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart})
        if value=="":
            response.delete_cookie('product_ids')
        response.set_cookie('product_ids',value)
        return response

def checkout(request):
    return render(request,'ecom/checkout.html')

def productdetails(request,pk):
    product= models.Product.objects.filter(id=pk).first()
    return render(request, 'ecom/productdetails.html', {"product" : product})


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
