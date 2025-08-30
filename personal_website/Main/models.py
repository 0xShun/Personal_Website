from django.db import models
from django.utils import timezone
import markdown
from django.utils.text import slugify
from django.core.files.storage import default_storage
import os   

class ProjectCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class ArticleCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class ResearchCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=200)
    github_link = models.URLField(blank=True, null=True)
    categories = models.ManyToManyField(ProjectCategory, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Article(models.Model):

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    categories = models.ManyToManyField(ArticleCategory, blank=True)
    markdown_file = models.FileField(
        upload_to='articles/markdown/',
        help_text="Upload a Markdown (.md) file",
        null=True,
        blank=True
    )
    content_md = models.TextField(editable=False)
    content_html = models.TextField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Process markdown file if it has changed
        if self.markdown_file:
            try:
                # Read the markdown file content
                content = self.markdown_file.read().decode('utf-8')
                self.content_md = content
                
                # Convert markdown to HTML
                self.content_html = markdown.markdown(
                    content,
                    extensions=['extra', 'codehilite', 'toc']
                )
            except Exception as e:
                # If there's an error, set content to error message
                self.content_md = f"Error reading markdown file: {str(e)}"
                self.content_html = self.content_md

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the markdown file when the article is deleted
        if self.markdown_file:
            if os.path.isfile(self.markdown_file.path):
                os.remove(self.markdown_file.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Research(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200)
    abstract = models.TextField(blank=True, null=True, help_text="Optional for ongoing research")
    pdf_file = models.FileField(upload_to='research_pdfs/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    published_date = models.DateField(blank=True, null=True, help_text="Optional for ongoing research")
    categories = models.ManyToManyField(ResearchCategory, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def clean(self):
        """Custom validation to ensure completed research has required fields"""
        from django.core.exceptions import ValidationError
        
        if self.status == 'completed':
            if not self.abstract:
                raise ValidationError({'abstract': 'Abstract is required for completed research.'})
            if not self.published_date:
                raise ValidationError({'published_date': 'Published date is required for completed research.'})

    class Meta:
        ordering = ['-created_at']  # Changed to created_at since published_date can be null
        verbose_name_plural = "Research"

class CarouselImage(models.Model):
    image_url = models.URLField("Image URL", help_text="Paste a direct image link (e.g., Imgur)")
    title = models.CharField(max_length=100, blank=True)
    caption = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title or f"Carousel Image {self.pk}"


class Comment(models.Model):
    CONTENT_TYPES = (
        ('project', 'Project'),
        ('research', 'Research'),
        ('article', 'Article'),
    )
    
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    object_id = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    email = models.EmailField()  # Optional but useful for spam prevention
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # For moderation
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.name} on {self.content_type} {self.object_id}"
    
    def save(self, *args, **kwargs):
        # Basic sanitization (you'll need to install bleach)
        # from django.utils.html import strip_tags
        # import bleach
        # self.name = bleach.clean(strip_tags(self.name))
        # self.content = bleach.clean(self.content, 
        #                           tags=['p', 'br', 'strong', 'em'],
        #                           strip=True)
        
        # For now, just use strip_tags for basic sanitization
        from django.utils.html import strip_tags
        self.name = strip_tags(self.name)
        self.content = strip_tags(self.content)
        
        super().save(*args, **kwargs)

