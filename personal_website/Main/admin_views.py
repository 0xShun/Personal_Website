from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from .models import Project, Article, Research, CarouselImage

@staff_member_required
def custom_admin_index(request, extra_context=None):
    """
    Custom admin index view that adds model counts
    """
    app_list = []
    
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
    
    request.current_app = 'admin'
    
    return TemplateResponse(request, 'admin/index.html', context)
