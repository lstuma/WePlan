# Generated by Django 4.1.3 on 2022-11-12 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_task_end_task_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='duration',
            field=models.IntegerField(blank=True, default=None),
        ),
    ]
