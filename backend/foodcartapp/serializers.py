from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import IntegerField
from .models import Order, OrderedProduct


class OrderedProductSerializer(ModelSerializer):
    quantity = IntegerField()

    class Meta:
        model = OrderedProduct
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderedProductSerializer(
        many=True,
        allow_empty=False,
        write_only=True
    )

    def create(self, validated_data):
        order = Order.objects.create(
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            phonenumber=validated_data['phonenumber'],
            address=validated_data['address']
        )

        for serialize_product in validated_data['products']:
            order.products.create(
                product=serialize_product['product'],
                quantity=serialize_product['quantity'],
                order=order,
                price=serialize_product['product'].price
            )

        return order

    class Meta:
        model = Order
        fields = [
            'firstname',
            'lastname',
            'phonenumber',
            'address',
            'products',
        ]
