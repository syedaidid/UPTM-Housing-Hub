from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('post', '0009_fulltext_search'),  # depends on previous migration
    ]
    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE post_housingpost ADD SYSTEM VERSIONING;",
            reverse_sql="ALTER TABLE post_housingpost DROP SYSTEM VERSIONING;"
        )
    ]
