# Generated by Django 4.2.1 on 2023-06-18 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('craftapp', '0005_remove_video_video_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='description',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='picture',
            field=models.ImageField(default='static/assets/placeholder.jpg', upload_to=''),
        ),
    ]