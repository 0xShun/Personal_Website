from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carouselimage',
            name='image',
        ),
        migrations.AddField(
            model_name='carouselimage',
            name='image_url',
            field=models.URLField(default='', verbose_name='Image URL', help_text='Paste a direct image link (e.g., Imgur)'),
            preserve_default=False,
        ),
    ] 