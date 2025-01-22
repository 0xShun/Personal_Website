from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    github_link = models.URLField()
    cover_image = models.ImageField(upload_to='project_covers/')
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Research(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
