# Generated by Django 4.2.16 on 2024-11-17 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('followrequests', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='followrequest',
            unique_together=set(),
        ),
    ]