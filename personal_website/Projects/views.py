from django.shortcuts import render
from Main.models import Project

# Create your views here.
def projects(request):
    projects = Project.objects.all()
    context = {
        'projects': projects,
        'title': 'Projects'  # Adding title for the projects page
    }
    return render(request, 'projects.html', context)
