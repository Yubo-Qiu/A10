# Generated by Django 5.1.2 on 2024-11-30 22:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0006_remove_permission_can_edit_impacts_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Impact",
        ),
    ]
