# Generated by Django 4.2.1 on 2023-05-19 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0002_alter_rating_value'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'ordering': ['-timestamp']},
        ),
    ]
