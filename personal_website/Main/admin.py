from django.contrib import admin
from .models import Project, Article, Research

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'technologies', 'github_link', 'created_at')
    search_fields = ('title', 'description', 'technologies')
    list_filter = ('category', 'created_at')
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Technical Details', {
            'fields': ('technologies', 'github_link')
        }),
    )
    list_editable = ('category',)  # Allow quick category changes from list view

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'updated_at')
    list_display_links = ('title',)
    search_fields = ('title',)
    list_filter = ('category', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('content_html', 'content_md')
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Article Information', {
            'fields': ('title', 'slug', 'category')
        }),
        ('Content', {
            'fields': ('markdown_file',),
            'description': 'Upload a Markdown (.md) file containing your article content.'
        }),
        ('Preview', {
            'fields': ('content_md', 'content_html'),
            'classes': ('collapse',),
            'description': 'Preview of the processed content (read-only)'
        })
    )
    list_editable = ('category',)  # Allow quick category changes from list view

    def save_model(self, request, obj, form, change):
        # Handle file upload and save
        super().save_model(request, obj, form, change)
        
        if 'markdown_file' in form.changed_data:
            obj.save()  # This will trigger the markdown processing in the model

@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'created_at')
    search_fields = ('title', 'abstract')
    list_filter = ('published_date', 'created_at')
    date_hierarchy = 'published_date'
    fieldsets = (
        ('Research Information', {
            'fields': ('title', 'abstract', 'published_date')
        }),
        ('File', {
            'fields': ('pdf_file',)
        }),
    )
