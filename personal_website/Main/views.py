from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.crypto import get_random_string
from django.core.cache import cache
from .models import Project, Research, Article
import os
from django.conf import settings
import logging
from django.urls import reverse
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    """
    View function for the home page.
    """
    # Debug static files
    logo_paths = []
    for static_dir in settings.STATICFILES_DIRS:
        potential_path = os.path.join(static_dir, 'images', 'logo.jpg')
        exists = os.path.exists(potential_path)
        logo_paths.append(f"Checking {potential_path}: {'Found' if exists else 'Not found'}")
    
    logger.info("Static file paths checked:\n" + "\n".join(logo_paths))
    
    context = {
        'title': 'Home'
    }
    return render(request, 'home.html', context)

def contact(request):
    """
    View function for the contact page.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Send email
        try:
            send_mail(
                f'Contact Form: {subject}',
                f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again later.')
            print(f"Error sending email: {str(e)}")

    return render(request, 'contact.html')

def login_view(request):
    """
    View function for handling user login using Django's built-in authentication forms.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    # Generate security token and additional random key
                    token = default_token_generator.make_token(user)
                    admin_key = get_random_string(32)
                    
                    # Store both in session and cache with expiry
                    request.session['admin_token'] = token
                    request.session['admin_key'] = admin_key
                    cache_key = f'admin_access_{user.id}'
                    cache.set(cache_key, admin_key, timeout=3600)  # 1 hour expiry
                    
                    login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect('home')
                else:
                    messages.error(request, 'Only administrators can access this page.')
                    return render(request, 'login.html', {'form': form})
            else:
                messages.error(request, 'Invalid username or password.')
                return render(request, 'login.html', {'form': form})
        else:
            messages.error(request, 'Please enter valid credentials.')
            return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()

    context = {
        'title': 'Login',
        'form': form
    }
    return render(request, 'login.html', context)

def superuser_required(user):
    """
    Custom check for superuser status
    """
    return user.is_superuser

@user_passes_test(lambda u: u.is_superuser and u.is_staff and u.is_active, login_url='login')
def admin(request):
    """
    View function for the admin page that handles both project and research uploads.
    Only accessible by active superusers who have access to Django's admin interface.
    Additional security checks are performed to prevent unauthorized access.
    """
    # Verify the user has a valid admin session
    if not request.user.is_authenticated or \
       not request.user.is_superuser or \
       not request.user.is_staff or \
       not request.user.is_active:
        messages.error(request, 'Unauthorized access.')
        return redirect('login')

    # Rate limiting check to prevent abuse
    rate_limit_key = f'admin_requests_{request.user.id}'
    request_count = cache.get(rate_limit_key, 0)
    if request_count > 100:  # 100 requests per hour limit
        messages.error(request, 'Too many requests. Please try again later.')
        return redirect('home')
    cache.set(rate_limit_key, request_count + 1, timeout=3600)

    if request.method == 'POST':
        # Handle project upload
        if 'project_title' in request.POST:
            title = request.POST.get('project_title')
            cover = request.FILES.get('project_cover')
            description = request.POST.get('project_description')
            github_link = request.POST.get('github_link')
            
            # Create new project
            project = Project(
                title=title,
                description=description,
                github_link=github_link,
                cover_image=cover
            )
            project.save()

        # Handle research upload
        elif 'research_file' in request.FILES:
            research_file = request.FILES['research_file']
            if research_file.name.endswith('.md'):
                # Read and process markdown file
                content = research_file.read().decode('utf-8')
                research = Research(
                    title=research_file.name.replace('.md', ''),
                    content=content
                )
                research.save()

    context = {
        'title': 'Admin Dashboard'
    }
    return render(request, 'admin.html', context)

@login_required(login_url='/gwapo_login')
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'admin/login.html')

@login_required(login_url='/gwapo_login')
def add_project(request):
    if request.method == 'POST':
        # Handle project creation
        title = request.POST.get('title')
        description = request.POST.get('description')
        technologies = request.POST.get('technologies')
        # Add your project creation logic here
        messages.success(request, 'Project added successfully')
        return redirect('admin_dashboard')
    return redirect('admin_dashboard')

@login_required(login_url='/gwapo_login')
def add_research(request):
    if request.method == 'POST':
        # Handle research creation
        title = request.POST.get('title')
        abstract = request.POST.get('abstract')
        published_date = request.POST.get('published_date')
        # Add your research creation logic here
        messages.success(request, 'Research added successfully')
        return redirect('admin_dashboard')
    return redirect('admin_dashboard')

@login_required(login_url='/gwapo_login')
def add_article(request):
    if request.method == 'POST':
        # Handle article creation
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        # Add your article creation logic here
        messages.success(request, 'Article added successfully')
        return redirect('admin_dashboard')
    return redirect('admin_dashboard')

def projects(request):
    projects = Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})

def research(request):
    research_list = Research.objects.all()
    return render(request, 'research.html', {'research_list': research_list})

def research_detail(request, pk):
    research = get_object_or_404(Research, pk=pk)
    return render(request, 'research_detail.html', {'research': research})

def articles(request):
    articles = Article.objects.all()
    return render(request, 'articles.html', {'articles': articles})

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'article_detail.html', {'article': article})
