# Generated by Django 4.2.5 on 2024-03-18 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0062_booking_is_acceped_booking_is_rejected_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='is_acceped',
            new_name='is_accepted',
        ),
        # migrations.DeleteModel(
        #     name='userprofile',
        # ),
    ]
