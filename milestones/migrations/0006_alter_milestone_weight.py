# Generated by Django 4.2.16 on 2024-11-11 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('milestones', '0005_milestone_age_months_milestone_age_years_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestone',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=1, help_text='Weight in kg', max_digits=4, null=True),
        ),
    ]
