# Generated by Django 5.2.1 on 2025-07-25 10:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_customer_sale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='sale_date',
        ),
        migrations.AddField(
            model_name='sale',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
