from django.db import models
# from froala_editor.fields import FroalaField
from tinymce.models import HTMLField
# from django_quill.fields import QuillField
from django.contrib.auth.models import User
from .helper import *

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length=100)

class blogmodel(models.Model):
    title = models.CharField(max_length=1500)
    content=HTMLField()
    slug=models.SlugField(max_length=1000,null=True,blank=True)
    image=models.ImageField(upload_to='media')
    created_at=models.DateTimeField( auto_now_add=True)
    updated_at=models.DateTimeField( auto_now=True)


    def __str__(self) -> str:
      return self.title

    def save(self, *args, **kwargs):
        self.slug= generate_slug(self.title)
        super(blogmodel,self).save(*args, **kwargs)