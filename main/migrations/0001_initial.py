# Generated by Django 4.1.3 on 2022-11-12 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taskid', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('qu', models.CharField(max_length=10)),
                ('outline_text', models.CharField(max_length=600)),
                ('detail_text', models.CharField(max_length=1500)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.project')),
                ('tasks', models.ManyToManyField(blank=True, to='main.task')),
            ],
        ),
    ]
