# Generated by Django 4.2.1 on 2023-06-19 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('craftapp', '0008_alter_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(default='/static/assets/placeholder.jpg', upload_to='images/profile_picture/'),
        ),
    ]