# Generated by Django 3.2.6 on 2021-08-14 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_contactpoint_times_used'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
