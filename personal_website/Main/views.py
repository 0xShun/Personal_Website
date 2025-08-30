from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.crypto import get_random_string
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Project, Research, Article, ArticleCategory, ProjectCategory, ResearchCategory, CarouselImage, Comment, Accolade
from .forms import CommentForm
import os
from django.conf import settings
import logging
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView

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
    
    images = CarouselImage.objects.order_by('order')
    accolades = Accolade.objects.filter(is_featured=True).order_by('-date_achieved')[:6]  # Show latest 6 featured accolades
    
    context = {
        'title': 'Home',
        'carousel_images': images,
        'accolades': accolades,
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
    category_filter = request.GET.get('category')
    if category_filter:
        projects = Project.objects.filter(categories__id=category_filter)
    else:
        projects = Project.objects.all()
    categories = ProjectCategory.objects.all()
    return render(request, 'projects.html', {'projects': projects, 'categories': categories, 'selected_category': category_filter})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    # Get approved comments
    comments = Comment.objects.filter(
        content_type='project',
        object_id=project.id,
        is_approved=True
    )
    
    # Comment form
    form = CommentForm()
    
    return render(request, 'project_detail.html', {
        'project': project,
        'comments': comments,
        'comment_form': form
    })

def research(request):
    category_filter = request.GET.get('category')
    if category_filter:
        research_list = Research.objects.filter(categories__id=category_filter)
    else:
        research_list = Research.objects.all()
    categories = ResearchCategory.objects.all()
    return render(request, 'research.html', {'research_list': research_list, 'categories': categories, 'selected_category': category_filter})

def research_detail(request, pk):
    research = get_object_or_404(Research, pk=pk)
    
    # Get approved comments
    comments = Comment.objects.filter(
        content_type='research',
        object_id=research.id,
        is_approved=True
    )
    
    # Comment form
    form = CommentForm()
    
    return render(request, 'research_detail.html', {
        'research': research,
        'comments': comments,
        'comment_form': form
    })

def articles(request):
    category_filter = request.GET.get('category')
    year_filter = request.GET.get('year')
    
    # Base queryset
    articles = Article.objects.all()
    
    # Apply category filter
    if category_filter:
        articles = articles.filter(categories__id=category_filter)
    
    # Apply year filter
    if year_filter:
        articles = articles.filter(created_at__year=year_filter)
    
    # Get all categories
    categories = ArticleCategory.objects.all()
    
    # Get available years from articles (ordered newest first)
    # Using a more compatible approach for getting years
    all_articles = Article.objects.all().order_by('-created_at')
    available_years = []
    seen_years = set()
    
    for article in all_articles:
        year = article.created_at.year
        if year not in seen_years:
            available_years.append(year)
            seen_years.add(year)
    
    return render(request, 'articles.html', {
        'articles': articles, 
        'categories': categories, 
        'selected_category': category_filter,
        'available_years': available_years,
        'selected_year': year_filter
    })

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    
    # Get approved comments
    comments = Comment.objects.filter(
        content_type='article',
        object_id=article.id,
        is_approved=True
    ).order_by('-created_at')
    
    # Comment form
    form = CommentForm()
    
    return render(request, 'article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form
    })

@require_POST
def post_comment(request, content_type, object_id):
    """
    Handle comment submissions with rate limiting and security checks
    Supports both AJAX and regular form submissions
    """
    # Get IP address for rate limiting
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    # Rate limiting - one comment per minute per IP
    cache_key = f'comment_ip_{ip}'
    last_comment_time = cache.get(cache_key)
    
    if last_comment_time and (timezone.now() - last_comment_time).total_seconds() < 60:
        error_msg = "Please wait a moment before posting another comment."
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': error_msg})
        messages.error(request, error_msg)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.content_type = content_type
        comment.object_id = object_id
        comment.ip_address = ip
        
        # Auto-approve for now, can set to False for moderation
        comment.is_approved = True
        comment.save()
        
        # Set rate limit
        cache.set(cache_key, timezone.now())
        
        success_msg = "Your comment has been submitted successfully!"
        
        # Handle AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True, 
                'message': success_msg,
                'comment': {
                    'name': comment.name,
                    'content': comment.content,
                    'created_at': comment.created_at.strftime('%B %d, %Y'),
                    'website': comment.website if comment.website else None
                }
            })
        
        messages.success(request, success_msg)
    else:
        # If the form is invalid, show the errors
        error_message = "There was an error with your comment submission. "
        for field, errors in form.errors.items():
            if field == 'honeypot':
                continue  # Don't show honeypot errors to users
            error_message += f"{', '.join(errors)} "
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': error_message.strip()})
            
        messages.error(request, error_message.strip())
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# Custom error handlers
def custom_404(request, exception):
    """Custom 404 page for when a page is not found"""
    return render(request, 'errors/404.html', status=404)

def custom_500(request):
    """Custom 500 page for server errors"""
    return render(request, 'errors/500.html', status=500)
