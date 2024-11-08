from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_alter_comment_milestone'),
    ]

    operations = [
        migrations.RunSQL(
            sql="UPDATE comments_comment SET milestone_id = 4 WHERE milestone_id IS NULL;",
            reverse_sql="UPDATE comments_comment SET milestone_id = NULL WHERE milestone_id = 4;"
        ),
    ]
