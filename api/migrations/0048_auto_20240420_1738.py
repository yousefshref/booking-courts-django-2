# Generated by Django 3.2.25 on 2024-04-20 15:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0047_auto_20240420_1705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='is_negative',
        ),
        migrations.AlterField(
            model_name='book',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 20, 17, 38, 51, 44054)),
        ),
    ]
