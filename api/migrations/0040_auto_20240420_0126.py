# Generated by Django 3.2.25 on 2024-04-19 23:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_alter_book_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academytime',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='academytime',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 20, 1, 26, 54, 449098)),
        ),
    ]