# Generated by Django 3.2.25 on 2024-04-20 13:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0040_auto_20240420_0126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='academytrainer',
            name='academy',
        ),
        migrations.AlterField(
            model_name='book',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 20, 15, 0, 29, 691773)),
        ),
    ]
