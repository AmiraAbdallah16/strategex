from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from authentication.data_scraper import scrape_data
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    return  render(request, "authentication/index.html")

def signup(request):

    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try other username")
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request, "Email already exist! Please try other Email")
            return redirect('signup')
        
        if len(username)>10:
            messages.error(request, "username must be under 10 characters")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "Username must be alpha-Numeric!")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        
        myuser.save()

        # messages.success(request, "Your Account created successfully.")

        return redirect("signin")

    return render(request, "authentication/signup.html")

def signin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request,user)
            fname = user.first_name
            return render(request, "authentication/userpage.html", {'fname' : fname})
        
        else:
            messages.error(request, "Username or Password is wrong")
            return redirect('signin')
            

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')

def userpage(request):
    return render(request, "authentication/userpage.html")

def scrape_data_view(request):
    country = request.GET.get('country')
    contents = request.GET.get('contents')
    scrape_data(country, contents)
    return HttpResponse('Data scraped successfully')