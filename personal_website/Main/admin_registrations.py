from django.contrib import admin
from django.contrib.auth.models import User, Group
from .admin_site import custom_admin_site
from .models import Project, Article, Research, ProjectCategory, ArticleCategory, ResearchCategory, CarouselImage
from .admin import ProjectAdmin, ArticleAdmin, ResearchAdmin, ProjectCategoryAdmin, ArticleCategoryAdmin, ResearchCategoryAdmin, CarouselImageAdmin

# Register models with our custom admin site
custom_admin_site.register(User, admin.ModelAdmin)
custom_admin_site.register(Group, admin.ModelAdmin)
custom_admin_site.register(Project, ProjectAdmin)
custom_admin_site.register(Article, ArticleAdmin)
custom_admin_site.register(Research, ResearchAdmin)
custom_admin_site.register(ProjectCategory, ProjectCategoryAdmin)
custom_admin_site.register(ArticleCategory, ArticleCategoryAdmin)
custom_admin_site.register(ResearchCategory, ResearchCategoryAdmin)
custom_admin_site.register(CarouselImage, CarouselImageAdmin)
