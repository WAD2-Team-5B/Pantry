# Generated by Django 2.2.28 on 2024-03-01 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pantry', '0002_remove_userprofile_photourl'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='photoURL',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
