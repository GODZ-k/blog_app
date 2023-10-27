
from django.urls import path
from .views import *




urlpatterns = [
path('',home,name="home"),
path('login/',login_page,name="login_page"),
path('signup/',signup_page,name="signup_page"),
path('logout/',logout_page,name="logout_page"),
path('add_blog/',add_blog,name="add_blog"),
path('blog_detail/<slug>/',blog_details,name="blog_detail"),
path('blog_update/<slug>/',update_blog,name="blog_update"),
path('blog_delete/<id>',blog_delete,name="blog_delete"),
path('see_blog/',see_blog,name="see_blog")


]
