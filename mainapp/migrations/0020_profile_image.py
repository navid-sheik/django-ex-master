# Generated by Django 3.2.9 on 2021-12-07 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0019_auto_20211206_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default_profile.png', upload_to='profile_images'),
        ),
    ]
