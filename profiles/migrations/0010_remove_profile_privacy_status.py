# Generated by Django 4.2.16 on 2024-11-22 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_profile_privacy_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='privacy_status',
        ),
    ]
