from django.shortcuts import render

# Create your views here.
def home(request):
    """
    View function for the home page.
    """
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
