# Generated by Django 5.0.3 on 2024-07-01 19:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('activities', '0008_activitygroup_created_at_activitygroup_updated_at'),
        ('profiles', '0002_rename_profile_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecentActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('complete_report', 'complete_report'), ('delete_report', 'delete_report'), ('edit_report', 'edit_report')], max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.activity')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile')),
            ],
        ),
    ]
