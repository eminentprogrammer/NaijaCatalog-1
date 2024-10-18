# Generated by Django 5.1.1 on 2024-10-17 23:18

import cloudinary.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='NaijaCatalog/institution/logo/')),
                ('name', models.CharField(blank=True, max_length=500)),
                ('location', models.CharField(blank=True, max_length=500)),
                ('contact_email', models.EmailField(blank=True, max_length=254)),
                ('contact_phone', models.CharField(blank=True, max_length=15)),
                ('gmap', models.CharField(blank=True, max_length=1000)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('admin', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='institution', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Institutions',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('institution', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='partners.institution')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Students',
            },
        ),
    ]
