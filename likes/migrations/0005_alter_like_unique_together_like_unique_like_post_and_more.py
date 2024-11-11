# Generated by Django 4.2.16 on 2024-11-11 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0004_alter_like_milestone'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='like',
            constraint=models.UniqueConstraint(fields=('owner', 'post'), name='unique_like_post'),
        ),
        migrations.AddConstraint(
            model_name='like',
            constraint=models.UniqueConstraint(fields=('owner', 'milestone'), name='unique_like_milestone'),
        ),
    ]
