from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import user_passes_test
from django.utils.crypto import get_random_string
from django.core.cache import cache
from .models import Project, Tag, Research
import os
from django.conf import settings
import logging

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
    context = {
        'title': 'Contact'
    }
    return render(request, 'contact.html', context)

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
            tags = request.POST.get('project_tags')
            
            # Create new project
            project = Project(
                title=title,
                description=description,
                github_link=github_link,
                cover_image=cover
            )
            project.save()

            # Handle tags
            if tags:
                tag_list = [tag.strip() for tag in tags.split(',')]
                for tag_name in tag_list:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    project.tags.add(tag)

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
