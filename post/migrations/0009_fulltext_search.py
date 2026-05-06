from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('post', '0008_alter_housingpost_accessibilities_and_more'),
    ]
    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE post_housingpost ADD FULLTEXT INDEX ft_search (title, description, address);",
            reverse_sql="ALTER TABLE post_housingpost DROP INDEX ft_search;"
        )
    ]
