# Generated by Django 4.2.5 on 2024-02-29 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0051_fitnesscenter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitnesscenter',
            name='latitude',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='fitnesscenter',
            name='longitude',
            field=models.CharField(max_length=20),
        ),
    ]
