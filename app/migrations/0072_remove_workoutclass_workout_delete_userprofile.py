# Generated by Django 4.2.5 on 2024-04-08 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0071_remove_workoutclass_workout_details_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workoutclass',
            name='workout',
        ),
        #migrations.DeleteModel(
            #name='userprofile',
        #),
    ]
