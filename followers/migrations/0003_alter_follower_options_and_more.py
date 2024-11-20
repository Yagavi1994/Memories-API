# Generated by Django 4.2.16 on 2024-11-20 11:20

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('followers', '0002_alter_follower_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follower',
            options={'ordering': ['-created_at']},
        ),
        migrations.RemoveConstraint(
            model_name='follower',
            name='unique_follower',
        ),
        migrations.AlterUniqueTogether(
            name='follower',
            unique_together={('owner', 'followed')},
        ),
    ]