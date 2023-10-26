# from django import forms
# # from django_quill.forms import QuillFormField
# from blogapp.models import QuillPost

# class QuillPostForm(forms.ModelForm):
#     class Meta:
#         model = QuillPost
#         fields = (
#             'content',
#         )


from django import forms
from tinymce.widgets import TinyMCE
from .models import *

class blogform(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 20}))

    class Meta:
        model = blogmodel
        fields = ['content']