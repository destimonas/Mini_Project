# Generated by Django 4.2.5 on 2023-11-15 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_remove_timeslot_trainer_remove_trainer_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='trainer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.trainer'),
        ),
        migrations.AlterField(
            model_name='trainer',
            name='time_slots',
            field=models.ManyToManyField(related_name='trainers', to='app.timeslot'),
        ),
    ]
