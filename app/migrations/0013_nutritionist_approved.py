# Generated by Django 4.2.5 on 2023-11-06 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_trainer_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='nutritionist',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
