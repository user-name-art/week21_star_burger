from django.db import models
from django.utils import timezone
from django.db.models import Sum, F
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name='ресторан',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):
    def order_price(self):
        return self.annotate(
            total_price=Sum(F('products__quantity') * F('products__price'))
        )


class Order(models.Model):
    STATUS_ORDER = (
        (1, 'Необработанный'),
        (2, 'Готовится'),
        (3, 'Доставка'),
        (4, 'Выполнен'),
    )
    PAYMENT_ORDER = (
        (1, 'Наличные'),
        (2, 'Электронно'),
    )

    firstname = models.CharField(
        max_length=20,
        verbose_name='имя',
        null=False
    )
    lastname = models.CharField(
        max_length=20,
        verbose_name='фамилия',
        null=False
    )
    phonenumber = PhoneNumberField('телефон', db_index=True)
    address = models.CharField(
        max_length=50,
        verbose_name='адрес',
        null=False
    )
    status = models.IntegerField(
        verbose_name='статус заказа',
        choices=STATUS_ORDER,
        default=1,
        db_index=True
    )
    payment_method = models.IntegerField(
        verbose_name='способ оплаты',
        choices=PAYMENT_ORDER,
        null=True,
        db_index=True
    )
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField(
        verbose_name='время создания заказа',
        default=timezone.now,
        db_index=True
    )
    processed_at = models.DateTimeField(
        verbose_name='время подтверждения заказа',
        null=True,
        blank=True,
        db_index=True
    )
    delivered_at = models.DateTimeField(
        verbose_name='время доставки заказа',
        null=True,
        blank=True,
        db_index=True
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname}, {self.address}'


class OrderedProduct(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='блюдо',
        related_name='ordered_products'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='заказ',
        related_name='products'
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='количество'
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'блюдо в заказе'
        verbose_name_plural = 'блюда в заказе'

    def __str__(self):
        return f'{self.product.name} - {self.order}'
