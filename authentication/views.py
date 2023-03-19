from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from authentication.data_scraper import scrape_data
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import rotate_token

# Create your views here.
@csrf_protect
def home(request):
    return  render(request, "authentication/index.html")

@csrf_protect
def signup(request):

    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if User.objects.filter(username=username):
            messages.add_message(request,messages.SUCCESS, "Username already exist! Please try other username")
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.add_message(request,messages.SUCCESS, "Email already exist! Please try other Email")
            return redirect('signup')
        
        if len(username)>10:
            messages.add_message(request,messages.SUCCESS, "username must be under 10 characters")
            return redirect('signup')

        if pass1 != pass2:
            messages.add_message(request,messages.SUCCESS, "Passwords didn't match")
            return redirect('signup')

        if not username.isalnum():
            messages.add_message(request,messages.SUCCESS, "Username must be alpha-Numeric!")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        
        myuser.save()

        # messages.success(request, "Your Account created successfully.")

        return redirect("signin")

    return render(request, "authentication/signup.html")

@csrf_protect
def signin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            rotate_token(request)
            login(request,user)
            fname = user.first_name
            return render(request, "authentication/userpage.html", {'fname' : fname})
        
        else:
            messages.add_message(request,messages.SUCCESS, "Username or Password is wrong")
            return redirect('signin')
            

    return render(request, "authentication/signin.html")

@csrf_protect
def signout(request):
    rotate_token(request)
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')

@csrf_protect
def userpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            rotate_token(request)
            login(request,user)
            username = request.user.username
            return render(request, "authentication/userpage.html" , {'username' : username.capitalize()})
        else:
            messages.add_message(request,messages.SUCCESS, "Username or Password is wrong")
            return redirect('signin')
        
    return render(request, "authentication/signin.html")
        
@csrf_protect
def scrape_data_view(request):
    country = request.GET.get('country')
    contents = request.GET.get('contents')
    scrape_data(country, contents)
    messages.add_message(request, messages.SUCCESS, 'data downloaded')
    return userpage(request)
