# Generated by Django 5.0.3 on 2024-03-16 14:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_reportactivity_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.AddField(
            model_name='activity',
            name='activity_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='activities.activitygroup'),
        ),
    ]