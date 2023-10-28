from django.shortcuts import render,redirect
from blogapp.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from blogapp.forms import *
from blogapp.helper import *
# from blogapp.forms import QuillPostForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    try:
     blog_content=blogmodel.objects.all()
     data={
        'blog': blog_content
     }
    except Exception as e:
        print(e)

    return render(request, 'home.html', data)

@login_required(login_url="/login/")
def blog_details(request,slug):
    try:
     blog_obj=blogmodel.objects.filter(slug=slug).first()
     context={
        'blog': blog_obj
     }
    except Exception as e:
        print(e)
    return render(request, 'blog_detail.html',context)

@login_required(login_url="/login/")
def see_blog(request):
    try:
     blog_objs=blogmodel.objects.filter(user=request.user)
     context={
        'blog_objs': blog_objs
     }
    except Exception as e:
        print(e)
    return render(request, 'see_blog.html',context)


@login_required(login_url="/login/")
def blog_delete(request,id):
    try:
     delete_blog=blogmodel.objects.get(id=id)
     if delete_blog.user == request.user:
         delete_blog.delete()
     else:
         return redirect("/see_blog/")
    except Exception as e:
        print(e)

    return redirect("/")
@login_required(login_url="/login/")
def update_blog(request,slug):  # sourcery skip: extract-method
    try:
     blog_objs=blogmodel.objects.get(slug=slug)
     if blog_objs.user != request.user:
        return redirect("/")

     initial_dict={
        'content': blog_objs.content
     }
     form=blogform(initial=initial_dict)
     if request.method == 'POST':
      form=blogform(request.POST)
      title=request.POST.get('title')
      image=request.FILES.get('image')
      user=request.user
      if form.is_valid():
        content=form.cleaned_data['content']
      blog_objs= blogmodel.objects.create(
        user=user,
        title=title, image=image,content=content
        )

     context={
       "blog_objs": blog_objs,
       'form':form

     }
    except Exception as e:
     print(e)
    return render(request,"update_blog.html",context)

def login_page(request):
    try:
     if request.method == 'POST':
        username=request.POST.get('loginUsername')
        password=request.POST.get('loginPassword')

        user_username=User.objects.filter(username=username)
        if not user_username.exists():
            messages.error(request,"Invalid username")
            return redirect("/login/")

        elif not Profile.objects.filter(user=user_username).first().is_verified:
            messages.error(request,"Your profile isn't verified")
            return redirect("/login/")

        elif user_username := authenticate(username=user_username, password=password):
            login(request,user_username)
            messages.success(request,"See you soon")
            return redirect('/')

        else:
            messages.error(request,"Invalid password")
            return redirect('/login/')
    except Exception as e:
      print(e)

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


    user_obj=User.objects.create(username=username)
    user_obj.set_password(password)
    user_obj.save()
    token=generate_random_string(20)
    Profile.objects.create(user=user_obj,token=token)
    send_main(token,username)
    messages.success(request,"Account Created succesfully")
    return redirect('/login/')

def logout_page(request):
    logout(request)
    return redirect("/login/")

@login_required(login_url="/login/")
def add_blog(request):
    try:
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
    except Exception as e:
        print(e)
    return render(request,'add_blog.html',context)


def verify(request,token):
    try:
        if Profile_obj := Profile.objects.filter(token=token).first():
            Profile_obj.is_verified=True
            Profile_obj.save()
        return redirect("/login/")
    except Exception as e:
        print(e)

