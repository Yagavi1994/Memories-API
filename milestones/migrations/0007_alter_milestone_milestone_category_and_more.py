# Generated by Django 4.2.16 on 2024-11-12 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('milestones', '0006_alter_milestone_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestone',
            name='milestone_category',
            field=models.CharField(choices=[('physical', 'Physical'), ('cognitive', 'Cognitive'), ('emotional', 'Emotional'), ('social', 'Social'), ('motor', 'Motor'), ('language', 'Language'), ('other', 'Other')], default='other', help_text='Category of the milestone', max_length=20),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='milestone_date',
            field=models.DateField(blank=True),
        ),
    ]
