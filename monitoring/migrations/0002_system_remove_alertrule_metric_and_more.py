# Generated by Django 5.2.1 on 2025-05-24 22:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='alertrule',
            name='metric',
        ),
        migrations.RemoveField(
            model_name='alertrule',
            name='notify_via',
        ),
        migrations.AddField(
            model_name='alertrule',
            name='metric_name',
            field=models.CharField(default='cpu_usage', max_length=100),
        ),
        migrations.AddField(
            model_name='alertrule',
            name='notify_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='metric',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AddField(
            model_name='alertrule',
            name='system',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='alert_rules', to='monitoring.system'),
        ),
        migrations.AddField(
            model_name='metric',
            name='system',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='metrics', to='monitoring.system'),
        ),
        migrations.AlterUniqueTogether(
            name='metric',
            unique_together={('system', 'name', 'timestamp')},
        ),
        migrations.RemoveField(
            model_name='metric',
            name='description',
        ),
    ]
