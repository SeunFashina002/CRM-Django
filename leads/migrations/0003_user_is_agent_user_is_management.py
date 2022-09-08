# Generated by Django 4.0.5 on 2022-08-21 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_userprofile_agent_managed_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_agent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_management',
            field=models.BooleanField(default=True),
        ),
    ]
