# Generated by Django 4.2 on 2023-04-25 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oursite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='photo',
            field=models.ImageField(null=True, upload_to='oursite/images/menuImages/'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='photo',
            field=models.ImageField(null=True, upload_to='oursite/images/restImages/'),
        ),
    ]
