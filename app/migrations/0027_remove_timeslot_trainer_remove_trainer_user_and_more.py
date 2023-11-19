# Generated by Django 4.2.5 on 2023-11-15 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_alter_trainer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslot',
            name='trainer',
        ),
        migrations.RemoveField(
            model_name='trainer',
            name='user',
        ),
        migrations.AddField(
            model_name='trainer',
            name='time_slots',
            field=models.ManyToManyField(to='app.timeslot'),
        ),
    ]
