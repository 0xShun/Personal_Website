from django.contrib import admin
from .models import Project, Article, Research, ProjectCategory, ArticleCategory, ResearchCategory
from django.contrib.admin import SimpleListFilter
from Articles.models import Tag

class TagFilter(SimpleListFilter):
    title = 'tags'
    parameter_name = 'tags'

    def lookups(self, request, model_admin):
        return [(tag.id, tag.name) for tag in Tag.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tags__id__exact=self.value())
        return queryset

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'technologies', 'github_link', 'created_at')
    search_fields = ('title', 'description', 'technologies')
    list_filter = ('created_at', TagFilter)
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Technical Details', {
            'fields': ('technologies', 'github_link')
        }),
    )

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    list_display_links = ('title',)
    search_fields = ('title',)
    list_filter = ('created_at', TagFilter)
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
            'fields': ('title', 'abstract', 'published_date', 'category')
        }),
        ('File', {
            'fields': ('pdf_file',)
        }),
    )

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ResearchCategory)
class ResearchCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
