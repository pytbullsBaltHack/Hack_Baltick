# Generated by Django 2.2.7 on 2019-11-10 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webface', '0006_auto_20191110_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='real_user_id',
            field=models.IntegerField(default=0),
        ),
    ]
