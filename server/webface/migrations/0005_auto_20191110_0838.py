# Generated by Django 2.2.7 on 2019-11-10 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webface', '0004_auto_20191109_2240'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visitor',
            old_name='event',
            new_name='event_id',
        ),
    ]
