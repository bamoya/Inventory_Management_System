# Generated by Django 4.2.1 on 2023-06-03 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_rename_staff_profile_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='adress',
            new_name='address',
        ),
    ]