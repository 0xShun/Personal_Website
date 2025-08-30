from django.contrib import admin
from .models import Project, Article, Research, ProjectCategory, ArticleCategory, ResearchCategory, CarouselImage, Comment
from django.contrib.admin import SimpleListFilter
from Articles.models import Tag
from django import forms
from django.contrib.auth.models import User, Group
from .admin_site import custom_admin_site

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
    list_display = ('title', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'categories', 'created_at')
    search_fields = ('title', 'description')
    filter_horizontal = ('categories',)
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'categories', 'status')
        }),
        ('Technical Details', {
            'fields': ('technologies', 'github_link')
        }),
    )

class ArticleAdminForm(forms.ModelForm):
    created_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'step': '60'  # Allow minute precision
        }),
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M'],
        help_text="Leave blank to use current date/time"
    )
    
    updated_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'step': '60'  # Allow minute precision
        }),
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M'],
        help_text="Leave blank to use current date/time"
    )

    class Meta:
        model = Article
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial values for display if they exist
        if self.instance and self.instance.pk:
            if self.instance.created_at:
                self.fields['created_at'].initial = self.instance.created_at
            if self.instance.updated_at:
                self.fields['updated_at'].initial = self.instance.updated_at

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'created_at', 'updated_at')
    list_display_links = ('title',)
    search_fields = ('title',)
    list_filter = ('created_at', TagFilter)
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('content_html', 'content_md')
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Article Information', {
            'fields': ('title', 'slug', 'categories')
        }),
        ('Publishing Dates', {
            'fields': ('created_at', 'updated_at'),
            'description': 'Leave blank to use current date and time automatically.'
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

    class Media:
        css = {
            'all': ('admin/css/article_admin.css',)
        }
        js = ('admin/js/article_admin.js',)

class ResearchAdminForm(forms.ModelForm):
    CHOICES = (
        ('pdf', 'PDF File'),
        ('link', 'External Link'),
    )
    file_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False, label="Type")

    class Meta:
        model = Research
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial file_type based on which field is filled
        if self.instance and self.instance.link:
            self.fields['file_type'].initial = 'link'
        else:
            self.fields['file_type'].initial = 'pdf'
            
        # Make abstract and published_date optional by default in the form
        # Validation will be handled in clean() method based on status
        self.fields['abstract'].required = False
        self.fields['published_date'].required = False

    def clean(self):
        cleaned_data = super().clean()
        file_type = cleaned_data.get('file_type')
        pdf_file = cleaned_data.get('pdf_file')
        link = cleaned_data.get('link')
        status = cleaned_data.get('status')
        abstract = cleaned_data.get('abstract')
        published_date = cleaned_data.get('published_date')
        
        # File type validation
        if file_type == 'pdf' and not pdf_file:
            self.add_error('pdf_file', 'Please upload a PDF file or switch to link.')
        if file_type == 'link' and not link:
            self.add_error('link', 'Please provide a link or switch to PDF upload.')
            
        # Status-based validation for abstract and published_date
        if status == 'completed':
            if not abstract:
                self.add_error('abstract', 'Abstract is required for completed research.')
            if not published_date:
                self.add_error('published_date', 'Published date is required for completed research.')
        
        return cleaned_data

@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    form = ResearchAdminForm
    list_display = ('title', 'status', 'published_date', 'created_at', 'updated_at')
    list_filter = ('status', 'categories', 'created_at', 'published_date')
    search_fields = ('title', 'abstract')
    filter_horizontal = ('categories',)
    date_hierarchy = 'published_date'
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'status', 'categories'),
            'description': 'Basic research information and status'
        }),
        ('Content', {
            'fields': ('abstract', 'published_date'),
            'description': 'Note: Abstract and published date are optional for ongoing research'
        }),
        ('File/Link', {
            'fields': ('file_type', 'pdf_file', 'link'),
            'description': 'Choose whether to upload a PDF file or provide an external link'
        }),
    )

    class Media:
        js = ('admin/js/research_admin.js',)

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ResearchCategory)
class ResearchCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order', 'image_preview')
    ordering = ('order',)
    readonly_fields = ('image_preview',)
    fields = ('image_url', 'title', 'caption', 'order', 'image_preview')

    def image_preview(self, obj):
        if obj.image_url:
            return f'<img src="{obj.image_url}" style="max-height:60px; max-width:120px; border-radius:6px;" />'
        return ""
    image_preview.allow_tags = True
    image_preview.short_description = "Preview"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'object_id', 'created_at', 'is_approved')
    list_filter = ('content_type', 'is_approved', 'created_at')
    search_fields = ('name', 'email', 'content')
    readonly_fields = ('ip_address',)
    actions = ['approve_comments', 'reject_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"
    
    def reject_comments(self, request, queryset):
        queryset.delete()
    reject_comments.short_description = "Delete selected comments"
