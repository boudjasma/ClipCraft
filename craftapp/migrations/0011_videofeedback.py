# Generated by Django 4.2.1 on 2023-06-23 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('craftapp', '0010_alter_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(default=5)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='craftapp.video')),
            ],
        ),
    ]
