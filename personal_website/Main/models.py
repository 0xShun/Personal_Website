from django.db import models
from django.utils import timezone
import markdown
from django.utils.text import slugify
from django.core.files.storage import default_storage
from cloudinary_storage.storage import RawMediaCloudinaryStorage
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
    description = models.TextField(max_length=500, default="", help_text="Brief description to show in article listing (max 500 characters)")
    slug = models.SlugField(unique=True, blank=True)
    categories = models.ManyToManyField(ArticleCategory, blank=True)
    markdown_file = models.FileField(
        upload_to='articles/markdown/',
        storage=RawMediaCloudinaryStorage(),  # Store markdown in Cloudinary as raw files
        help_text="Upload a Markdown (.md) file",
        null=True,
        blank=True
    )
    content_md = models.TextField(editable=False)
    content_html = models.TextField(editable=False)
    created_at = models.DateTimeField(blank=True, null=True, help_text="Leave blank to use current date/time")
    updated_at = models.DateTimeField(blank=True, null=True, help_text="Leave blank to use current date/time")

    def save(self, *args, **kwargs):
        from django.utils import timezone
        
        # Set created_at if not provided (only for new objects)
        if not self.pk and not self.created_at:
            self.created_at = timezone.now()
            
        # Set updated_at if not provided
        if not self.updated_at:
            self.updated_at = timezone.now()
        
        # Generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Process markdown file only when a new file is uploaded or changed
        process_markdown = False
        if self.markdown_file:
            if not self.pk:
                process_markdown = True
            else:
                try:
                    old = Article.objects.get(pk=self.pk)
                    old_name = getattr(old.markdown_file, 'name', None)
                    new_name = getattr(self.markdown_file, 'name', None)
                    process_markdown = old_name != new_name
                except Article.DoesNotExist:
                    process_markdown = True

        if process_markdown and self.markdown_file:
            try:
                raw = self.markdown_file.read()
                content = raw if isinstance(raw, str) else raw.decode('utf-8')
                self.content_md = content

                # Convert markdown to HTML
                self.content_html = markdown.markdown(
                    content,
                    extensions=['extra', 'codehilite', 'toc']
                )
                # Reset file pointer so storage can save the file content
                try:
                    self.markdown_file.seek(0)
                except Exception:
                    pass
            except Exception as e:
                # If there's an error, set content to error message
                self.content_md = f"Error reading markdown file: {str(e)}"
                self.content_html = self.content_md

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the markdown file via the storage backend (Cloudinary) on delete
        if self.markdown_file:
            try:
                self.markdown_file.delete(save=False)
            except Exception:
                pass
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
    website = models.URLField(blank=True, null=True, help_text="Your website (optional)")
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


class Accolade(models.Model):
    title = models.CharField(max_length=200, help_text="Title of the accolade (e.g., '2nd Runner Up, HackForGov Regionals 2023')")
    description = models.TextField(help_text="Description of the achievement and competition details")
    date_achieved = models.DateField(help_text="Date when this accolade was achieved")
    organization = models.CharField(max_length=200, blank=True, help_text="Organization that hosted the competition (optional)")
    position = models.CharField(max_length=100, blank=True, help_text="Position achieved (e.g., '2nd Runner Up', 'Finalist', 'Top 6')")
    team_name = models.CharField(max_length=100, blank=True, help_text="Name of the team (if applicable)")
    is_featured = models.BooleanField(default=True, help_text="Display this accolade on the home page")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_achieved', '-created_at']
        verbose_name = "Accolade"
        verbose_name_plural = "Accolades"
    
    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    title = models.CharField(max_length=200, help_text="Title or caption for the image")
    description = models.TextField(blank=True, help_text="Optional description of the image")
    image = models.ImageField(upload_to='gallery/', help_text="Upload the gallery image")
    date_taken = models.DateField(blank=True, null=True, help_text="Date when the photo was taken (optional)")
    location = models.CharField(max_length=200, blank=True, help_text="Location where the photo was taken (optional)")
    category = models.CharField(
        max_length=50, 
        choices=[
            ('personal', 'Personal'),
            ('travel', 'Travel'),
            ('events', 'Events'),
            ('nature', 'Nature'),
            ('urban', 'Urban'),
            ('people', 'People'),
            ('other', 'Other'),
        ],
        default='other',
        help_text="Category of the image"
    )
    is_featured = models.BooleanField(default=True, help_text="Display this image in the gallery")
    order = models.PositiveIntegerField(default=0, help_text="Order of display (lower numbers appear first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
    
    def __str__(self):
        return self.title

