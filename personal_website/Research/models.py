from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class ResearchItem(models.Model):
    CATEGORY_CHOICES = [
        ('science', 'Science'),
        ('technology', 'Technology'),
        ('engineering', 'Engineering'),
        ('mathematics', 'Mathematics'),
    ]

    # Add other fields for the ResearchItem model
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='science'
    )
    tags = models.ManyToManyField(Tag, related_name='research_items')

    def __str__(self):
        return self.name  # Assuming there is a 'name' field
