from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import CharField
from .models import Order, OrderedProduct


class OrderedProductSerializer(ModelSerializer):
    quantity = CharField()

    class Meta:
        model = OrderedProduct
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderedProductSerializer(many=True, allow_empty=False, write_only=True)

    def create(self, validated_data):
        order = Order.objects.create(
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            phonenumber=validated_data['phonenumber'],
            address=validated_data['address']
        )

        for serialize_product in validated_data['products']:
            OrderedProduct.objects.create(
                product=serialize_product['product'],
                quantity=serialize_product['quantity'],
                order=order
            )

        return order

    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'phonenumber', 'address', 'products']
