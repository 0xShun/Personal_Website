# Generated by Django 4.2.7 on 2025-05-09 11:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Main", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="article",
            name="category",
        ),
        migrations.RemoveField(
            model_name="project",
            name="category",
        ),
        migrations.RemoveField(
            model_name="research",
            name="category",
        ),
        migrations.AddField(
            model_name="article",
            name="categories",
            field=models.ManyToManyField(blank=True, to="Main.articlecategory"),
        ),
        migrations.AddField(
            model_name="project",
            name="categories",
            field=models.ManyToManyField(blank=True, to="Main.projectcategory"),
        ),
        migrations.AddField(
            model_name="research",
            name="categories",
            field=models.ManyToManyField(blank=True, to="Main.researchcategory"),
        ),
    ]
