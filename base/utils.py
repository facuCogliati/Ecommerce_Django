from .models import *
import json

def cookieCart(request):
    try:
        card = json.loads(request.COOKIES['cart'])
        print(card)
    except:
        card = {}

    carrito = []
    order = {'total_cart': 0 , 'total_cart_items': 0}
    cardItems = order['total_cart_items']

    for x in card:
        order['total_cart_items'] += card[x]['quantity']
        product = Product.objects.get(id = x)
        total = (product.price * card[x]['quantity'])
        order['total_cart'] += total

        item = {
            'product' :{
            'id' : product.id,
            'name' : product.name,
            'image' : product.image,
            'price' : product.price,
            },
            'quantify' : card[x]['quantity'],
            'total_price' : total,
        }
        carrito.append(item)

    return {'carrito': carrito, 'order' : order,}