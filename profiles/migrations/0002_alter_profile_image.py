# Generated by Django 4.2.16 on 2024-11-04 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='images/default-profile-picture', upload_to='images/'),
        ),
    ]