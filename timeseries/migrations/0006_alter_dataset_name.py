# Generated by Django 5.0.3 on 2024-07-21 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeseries', '0005_dataset_task_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
