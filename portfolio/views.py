from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from .forms import BlogPostForm
from .models import BlogPost


class NewBlogs(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Desc")
    link = forms.CharField(label="link")

    
# Create your views here.
def index(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = BlogPostForm()

    blog_post = BlogPost.objects.all()
    for blog_data in blog_post:
        print(blog_data.description)
    return render(request, "portfolio/index.html", {
        "form": form,
        'blog_post': blog_post
    }) 

def blog(request):
    return HttpResponse("<h1>Welcome To My Blog!!</h1>")

def projects(request):
    return HttpResponse("Github Projects Here")



# Para han part na mag add hin new cards ha blog na tab

def addSecBlog(request):
    return render(request, "portfolio/SecurityBlog.html", {
        "form": NewBlogs()
    })
