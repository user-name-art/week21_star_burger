from django.http import JsonResponse
import json
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Order, OrderedProduct


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return Response(dumped_products)


@api_view(['POST'])
def register_order(request):
    received_order = request.data

    if 'products' in received_order and isinstance(received_order['products'], list) and received_order['products']:
        order = Order.objects.create(
            first_name=received_order['firstname'],
            last_name=received_order['lastname'],
            phonenumber=received_order['phonenumber'],
            address=received_order['address']
        )

        products = Product.objects.available()

        for product in received_order['products']:
            OrderedProduct.objects.create(
                product=products.get(id=product['product']),
                quantity=product['quantity'],
                order=order
            )
    else:
        return Response({'error': 'products must be non-empty list'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({})
