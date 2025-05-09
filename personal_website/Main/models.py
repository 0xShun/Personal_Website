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

    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=200)
    github_link = models.URLField(blank=True, null=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Article(models.Model):

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(ArticleCategory, on_delete=models.SET_NULL, null=True, blank=True)
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

    title = models.CharField(max_length=200)
    abstract = models.TextField()
    pdf_file = models.FileField(upload_to='research_pdfs/')
    published_date = models.DateField()
    category = models.ForeignKey(ResearchCategory, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date']
        verbose_name_plural = "Research"


