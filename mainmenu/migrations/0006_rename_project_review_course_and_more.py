# Generated by Django 4.1.5 on 2023-02-09 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainmenu', '0005_alter_video_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='project',
            new_name='course',
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('owner', 'course')},
        ),
    ]
