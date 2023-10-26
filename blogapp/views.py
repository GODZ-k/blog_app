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
    blog_content=blogmodel.objects.all()
    data={
        'blog': blog_content
    }

    return render(request, 'home.html', data)

@login_required(login_url="/login/")
def blog_details(request,slug):
    blog_obj=blogmodel.objects.filter(slug=slug).first()
    context={
        'blog': blog_obj
    }
    return render(request, 'blog_detail.html',context)
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

@login_required(login_url="/login/")
def add_blog(request):
    context={'form':blogform()}
    if request.method == 'POST':
        form=blogform(request.POST)
        title=request.POST.get('title')
        image=request.FILES.get('image')
        user=request.user
        if form.is_valid():
            content=form.cleaned_data['content']
        blogmodel.objects.create(
            user=user,
             title=title, image=image,content=content
            )
        return redirect("/add_blog/")
    return render(request,'add_blog.html',context)