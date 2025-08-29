from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

class CustomAdminSite(admin.AdminSite):
    site_header = 'Shawn\'s Admin'
    site_title = 'Shawn\'s Admin Portal'
    index_title = 'Dashboard'
    
    def each_context(self, request):
        context = super().each_context(request)
        context['site_url'] = reverse('home')
        return context
    
    def index(self, request, extra_context=None):
        # Override this to use our custom admin index
        from Main.admin_views import custom_admin_index
        return custom_admin_index(request, extra_context)

# Create a custom admin instance
custom_admin_site = CustomAdminSite(name='customadmin')
