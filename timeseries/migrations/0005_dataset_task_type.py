# Generated by Django 5.0.3 on 2024-07-20 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeseries', '0004_remove_dataset_task_type_alter_dataset_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='task_type',
            field=models.CharField(choices=[('regression', 'Regression'), ('classification', 'Classification')], default='regression', max_length=20),
        ),
    ]
