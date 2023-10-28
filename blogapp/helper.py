from django.utils.text import slugify



import random
import string

def generate_random_string(N):
        result = ''.join(random.choices(string.ascii_uppercase +string.digits, k=N))
        return result

def generate_slug(text):
    new_slug=slugify(text)
    from blogapp.models import blogmodel
    if blogmodel.objects.filter(slug=new_slug).first():
        return  generate_slug(text+generate_random_string(5))
    return new_slug

from blog import settings
from django.core.mail import send_mail
def send_main(token,email):
        subject = "your account needs to be verified"
        message=f"Hi paste the link to verify account http://127.0.0.1:8000/verify/{token}"
        email_from=settings.EMAIL_HOST_USER
        recipient_list=[email]
        send_mail(subject,message,email_from,recipient_list)
        return True