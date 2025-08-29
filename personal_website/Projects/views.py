from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from Main.models import Project, Comment, ProjectCategory
from Main.forms import CommentForm

# Create your views here.
def projects(request):
    projects = Project.objects.all()
    categories = ProjectCategory.objects.all()
    selected_category = request.GET.get('category')
    
    if selected_category:
        projects = projects.filter(categories__id=selected_category)
    
    context = {
        'projects': projects,
        'categories': categories,
        'selected_category': selected_category,
        'title': 'Projects'
    }
    return render(request, 'projects.html', context)

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Get comments for this project
    content_type = ContentType.objects.get_for_model(Project)
    comments = Comment.objects.filter(
        content_type=content_type,
        object_id=project.id,
        is_approved=True
    ).order_by('-created_at')
    
    # Comment form
    form = CommentForm()
    
    context = {
        'project': project,
        'comments': comments,
        'form': form,
        'title': project.title
    }
    
    return render(request, 'project_detail.html', context)
