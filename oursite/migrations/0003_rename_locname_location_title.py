# Generated by Django 4.2 on 2023-04-28 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oursite', '0002_alter_menu_photo_alter_restaurant_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='locName',
            new_name='title',
        ),
    ]
