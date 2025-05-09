from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    CATEGORY_CHOICES = [
        ('tutorial', 'Tutorials'),
        ('tech', 'Tech Reviews'),
        ('opinion', 'Opinion Pieces'),
    ]

    # Add other fields for the Article model
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='tutorial'
    )
    tags = models.ManyToManyField(Tag, related_name='articles')

    def __str__(self):
        return self.name  # Assuming there is a 'name' field
