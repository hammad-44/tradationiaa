from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.models import User 
from .models import Contact
from django.contrib.auth.decorators import user_passes_test

def user_not_authenticated(user):
    return not user.is_authenticated

# Apply the user_passes_test decorator to the view
def index(request):
    return render(request,"home/index.html")


def contact(request):
    if request.method =="POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        messsage = Contact( name = name,email = email,message=message)
        messsage.save()
        return render(request,"home/contact.html")
      
    else:
        return render(request,"home/contact.html")

def about(request):
    return render(request,"home/about.html")

def our_policy(request):
    return render(request,"home/our_policy.html")
def privacy_policy(request):
    return render(request,"home/privacy_policy.html")
def shipping_policy(request):
    return render(request,"home/shipping_policy.html")
def refund_policy(request):
    return render(request,"home/refund_policy.html")
def terms_conditions(request):
    return render(request,"home/terms_conditions.html")

def logouthandle(request):
    logout(request)
    return redirect('/')

@user_passes_test(user_not_authenticated, login_url='/')
def handlelogin(request):
    if request.method=="POST":
        loginemail=request.POST['email'].lower()
        loginpassword=request.POST['password']
        print(loginemail,loginpassword)
        user=authenticate(username=loginemail, password= loginpassword)
        print(loginemail,loginpassword)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, 'home/login.html')
        
    else:
        return render(request, 'home/login.html')


def signup(request):
    if request.method=="POST":
        email=request.POST['email']
        fname=request.POST['firstName']
        lname=request.POST['lastName']
        pass1=request.POST['password']
        username= email

        # Create the user
        myuser = User.objects.create_user(username,email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        return redirect('/')

    else:
        return render(request, 'home/signup.html')

def cart(request):
    return HttpResponse("HEllo cart")

def wishlist(request):
    return HttpResponse("HEllo World")


