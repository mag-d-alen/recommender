# Generated by Django 4.2.1 on 2023-05-18 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_alter_movie_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='last_updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='rating_avg',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='rating_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]