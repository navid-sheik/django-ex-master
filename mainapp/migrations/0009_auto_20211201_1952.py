# Generated by Django 3.2.9 on 2021-12-01 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_auto_20211201_1938'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hobby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='hobbies',
            field=models.ManyToManyField(blank=True, to='mainapp.Hobby'),
        ),
    ]
