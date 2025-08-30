from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _
from django.contrib.auth.models import User, Group
from .models import Project, Article, Research, ProjectCategory, ArticleCategory, ResearchCategory, CarouselImage, Comment, Accolade
from django.template.response import TemplateResponse

# Import admin classes from admin.py
from .admin import (
    ProjectAdmin, 
    ArticleAdmin, 
    ResearchAdmin, 
    ProjectCategoryAdmin, 
    ArticleCategoryAdmin, 
    ResearchCategoryAdmin, 
    CarouselImageAdmin,
    CommentAdmin,
    AccoladeAdmin
)

class CustomAdminSite(admin.AdminSite):
    site_header = 'Shawn\'s Admin'
    site_title = 'Shawn\'s Admin Portal'
    index_title = 'Dashboard'
    
    def each_context(self, request):
        context = super().each_context(request)
        context['site_url'] = reverse('home')
        return context
    
    def index(self, request, extra_context=None):
        """
        Custom admin index view that adds model counts
        """
        app_list = self.get_app_list(request)
        
        # Count objects for dashboard statistics
        project_count = Project.objects.count()
        article_count = Article.objects.count()
        research_count = Research.objects.count()
        carousel_count = CarouselImage.objects.count()

        context = {
            'title': _('Dashboard'),
            'app_list': app_list,
            'project_count': project_count,
            'article_count': article_count,
            'research_count': research_count,
            'carousel_count': carousel_count,
        }
        
        # Update with any extra context provided
        if extra_context:
            context.update(extra_context)
        
        request.current_app = self.name
        
        return TemplateResponse(request, 'admin/index.html', context)

# Create a custom admin instance
custom_admin_site = CustomAdminSite(name='customadmin')

# Register models with custom admin site
custom_admin_site.register(User, admin.ModelAdmin)
custom_admin_site.register(Group, admin.ModelAdmin)
custom_admin_site.register(Project, ProjectAdmin)
custom_admin_site.register(Article, ArticleAdmin)
custom_admin_site.register(Research, ResearchAdmin)
custom_admin_site.register(ProjectCategory, ProjectCategoryAdmin)
custom_admin_site.register(ArticleCategory, ArticleCategoryAdmin)
custom_admin_site.register(ResearchCategory, ResearchCategoryAdmin)
custom_admin_site.register(CarouselImage, CarouselImageAdmin)
custom_admin_site.register(Comment, CommentAdmin)
custom_admin_site.register(Accolade, AccoladeAdmin)
