# Generated by Django 4.2.5 on 2024-01-20 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_is_libraian_account_is_librarian'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=100),
        ),
    ]