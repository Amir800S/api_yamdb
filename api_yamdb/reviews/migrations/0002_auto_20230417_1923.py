# Generated by Django 3.2 on 2023-04-17 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='null', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[(1, 'moderator'), (2, 'user'), (3, 'admin')], default=2, max_length=15),
        ),
    ]