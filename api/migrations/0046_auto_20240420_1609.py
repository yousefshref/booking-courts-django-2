# Generated by Django 3.2.25 on 2024-04-20 14:09

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_auto_20240420_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academytrainer',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.academytype'),
        ),
        migrations.AlterField(
            model_name='book',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 20, 16, 9, 27, 935448)),
        ),
    ]