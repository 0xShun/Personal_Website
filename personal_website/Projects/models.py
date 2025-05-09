from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Web Development'),
        ('mobile', 'Mobile Apps'),
        ('ai', 'AI/ML'),
    ]

    # Add other fields for the Project model
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='web'
    )
    tags = models.ManyToManyField(Tag, related_name='projects')

    def __str__(self):
        return self.name  # Assuming there is a 'name' field
