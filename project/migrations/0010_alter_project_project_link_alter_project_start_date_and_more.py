# Generated by Django 5.1.2 on 2024-12-01 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0009_alter_profile_skills_alter_profile_social_links"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="project_link",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="start_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="tags",
            field=models.ManyToManyField(blank=True, null=True, to="project.tag"),
        ),
    ]
