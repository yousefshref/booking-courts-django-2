# Generated by Django 3.2.25 on 2024-04-13 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20240413_0654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='manager',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.managerprofile'),
        ),
    ]