from django.shortcuts import render,redirect
from blogapp.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from blogapp.forms import *
# from blogapp.forms import QuillPostForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request, 'home.html')

def login_page(request):
    try:
     if request.method == 'POST':
        username=request.POST.get('loginUsername')
        password=request.POST.get('loginPassword')

        user_username=User.objects.filter(username=username)
        if not user_username.exists():
            messages.error(request,"Invalid username")
            return redirect("/login/")

        if user_username := authenticate(username=username, password=password):
            login(request,user_username)
            messages.success(request,"Welcome")
            return redirect('/')

        else:
            messages.error(request,"Invalid password")
            return redirect('/login/')
    except:
     return redirect("/login/")

    return render(request, 'login.html')

def signup_page(request):  # sourcery skip: last-if-guard
    try:
        if request.method == 'POST':
            return _extracted_from_signup_page_4(request)
    except:
        return redirect("/signup/")
    return render(request, 'signup.html')


# TODO Rename this here and in `signup_page`
def _extracted_from_signup_page_4(request):
    username=request.POST.get('username')
    password=request.POST.get('password')

    user_name=User.objects.filter(username=username)
    if user_name.exists():
        messages.warning(request,"Username already exists")

    user=User.objects.create(username=username)
    user.set_password(password)
    user.save()
    messages.success(request,"Account Created succesfully")
    return redirect('/login/')

def logout_page(request):
    logout(request)
    return redirect("/login/")


def add_blog(request):
    context={'form':YourModelForm()}
    return render(request,'add_blog.html',context)