# Generated by Django 4.2.1 on 2023-05-15 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_rename_releaseset_date_movie_release_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
