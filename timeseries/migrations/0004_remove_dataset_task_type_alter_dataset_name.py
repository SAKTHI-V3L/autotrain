# Generated by Django 5.0.3 on 2024-07-20 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeseries', '0003_dataset_task_type_alter_dataset_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='task_type',
        ),
        migrations.AlterField(
            model_name='dataset',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
