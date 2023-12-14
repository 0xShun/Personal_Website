from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'description', 'link']


        widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Blog Title'}),
        'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Description'}),
        'link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Blog Link'}),
        }