# Generated by Django 2.2.7 on 2019-11-09 15:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webface', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamsource',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
