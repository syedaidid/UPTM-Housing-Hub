# Generated by Django 5.0.1 on 2024-03-10 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0003_housingpost_accessibility"),
    ]

    operations = [
        migrations.RenameField(
            model_name="housingpost",
            old_name="accessibility",
            new_name="accessibilities",
        ),
    ]
