# Generated by Django 5.2.1 on 2025-07-25 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_remove_sale_sale_date_sale_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='invoice_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
