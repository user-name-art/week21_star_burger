# Generated by Django 3.2.15 on 2024-01-19 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0048_alter_order_designated_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='designated_restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='restaurant', to='foodcartapp.restaurant', verbose_name='назваченный ресторан'),
        ),
    ]
