# Generated by Django 2.2 on 2019-06-08 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_manager', '0004_event_event_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_venue',
            field=models.CharField(default='Central Garden', max_length=100),
            preserve_default=False,
        ),
    ]
