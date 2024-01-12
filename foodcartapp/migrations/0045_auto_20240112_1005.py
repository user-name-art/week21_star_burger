# Generated by Django 3.2.15 on 2024-01-12 10:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0044_alter_order_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2024, 1, 12, 10, 5, 0, 142737, tzinfo=utc), verbose_name='время создания заказа'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivered_at',
            field=models.DateTimeField(db_index=True, null=True, verbose_name='время доставки заказа'),
        ),
        migrations.AddField(
            model_name='order',
            name='processed_at',
            field=models.DateTimeField(db_index=True, null=True, verbose_name='время подтверждения заказа'),
        ),
    ]
