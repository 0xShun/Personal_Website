from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from Main.models import Research, Comment
from Main.forms import CommentForm

# Create your views here.
def research(request):
    # Order by published_date (nulls last) then by created_at for ongoing research
    papers = Research.objects.all().order_by('-published_date', '-created_at')
    context = {
        'papers': papers,
        'title': 'Research'
    }
    return render(request, 'research.html', context)

def research_detail(request, paper_id):
    paper = get_object_or_404(Research, id=paper_id)
    
    # Get comments for this paper
    content_type = ContentType.objects.get_for_model(Research)
    comments = Comment.objects.filter(
        content_type=content_type,
        object_id=paper.id,
        is_approved=True
    ).order_by('-created_at')
    
    # Comment form
    form = CommentForm()
    
    context = {
        'paper': paper,
        'comments': comments,
        'form': form,
        'title': paper.title
    }
    
    return render(request, 'research_detail.html', context)