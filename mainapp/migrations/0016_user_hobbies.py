# Generated by Django 3.2.9 on 2021-12-01 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_remove_user_hobbies'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hobbies',
            field=models.ManyToManyField(blank=True, to='mainapp.Hobby'),
        ),
    ]