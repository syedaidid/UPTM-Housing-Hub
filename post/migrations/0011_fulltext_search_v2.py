from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('post', '0009_fulltext_search'),
    ]
    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE post_housingpost DROP INDEX ft_search;
                ALTER TABLE post_housingpost ADD FULLTEXT INDEX ft_search 
                (title, description, address, facilities, accessibilities, furnished, furnished_type, gender);
            """,
            reverse_sql="""
                ALTER TABLE post_housingpost DROP INDEX ft_search;
                ALTER TABLE post_housingpost ADD FULLTEXT INDEX ft_search 
                (title, description, address);
            """
        )
    ]
