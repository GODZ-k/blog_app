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
