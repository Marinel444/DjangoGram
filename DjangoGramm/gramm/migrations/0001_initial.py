# Generated by Django 4.2.1 on 2023-06-21 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('bio', models.TextField(blank=True)),
                ('photo', models.ImageField(blank=True, upload_to='user_photos')),
            ],
        ),
    ]
