# Generated by Django 4.2.1 on 2023-05-25 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('craftapp', '0003_profile_first_name_profile_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
