# Generated by Django 4.2 on 2023-04-28 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oursite', '0003_rename_locname_location_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='current_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='oursite.location'),
        ),
    ]
