# Generated by Django 3.2.15 on 2024-01-12 11:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0045_auto_20240112_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.IntegerField(blank=True, choices=[(1, 'Наличные'), (2, 'Электронно')], db_index=True, null=True, verbose_name='способ оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='время создания заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivered_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='время доставки заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='processed_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='время подтверждения заказа'),
        ),
    ]
