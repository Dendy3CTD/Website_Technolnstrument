# Generated manually: добавлено поле image в Category

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_load_initial_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.URLField(blank=True, max_length=500, verbose_name='URL изображения'),
        ),
    ]
