# Generated by Django 5.0.3 on 2024-03-16 15:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0007_activitygroup_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitygroup',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activitygroup',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
