# Generated by Django 3.2.25 on 2024-04-20 22:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0048_auto_20240420_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 21, 0, 28, 27, 432510)),
        ),
    ]
