# Generated by Django 2.2.28 on 2024-03-04 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pantry', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='cook_time',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='cuisine',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='date_pub',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='desc',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='difficulty',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='no_of_saves',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='prep_time',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='star_count',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='star_submissions',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='steps',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='user',
        ),
    ]
