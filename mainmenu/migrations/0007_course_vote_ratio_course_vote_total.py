# Generated by Django 4.1.5 on 2023-02-09 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainmenu', '0006_rename_project_review_course_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='vote_ratio',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='vote_total',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
