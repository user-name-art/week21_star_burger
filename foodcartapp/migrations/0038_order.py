# Generated by Django 3.2.15 on 2023-12-28 21:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0037_auto_20210125_1833'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(db_index=True, max_length=20, validators=[django.core.validators.MinValueValidator(0)], verbose_name='имя')),
                ('last_name', models.CharField(db_index=True, max_length=20, validators=[django.core.validators.MinValueValidator(0)], verbose_name='фамилия')),
                ('phonenumber', phonenumber_field.modelfields.PhoneNumberField(db_index=True, max_length=128, region=None, verbose_name='телефон')),
                ('address', models.CharField(max_length=50, validators=[django.core.validators.MinValueValidator(0)], verbose_name='адрес')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='foodcartapp.product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
    ]
