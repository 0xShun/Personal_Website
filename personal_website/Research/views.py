from django.shortcuts import render

# Create your views here.
def research(request):
    return render(request, 'research.html')