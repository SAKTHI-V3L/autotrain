# Generated by Django 5.0.3 on 2024-07-21 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeseries', '0006_alter_dataset_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='task_type',
        ),
    ]
