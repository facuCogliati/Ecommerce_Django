import json, datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from .utils import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .form import ClientCreation


# Create your views here.

def home(request):
    products = Product.objects.all()

    if request.user.is_authenticated:
        client = request.user.client
        order, create = Order.objects.get_or_create(client = client, complete=False)
        carrito = order.orderitems_set.all()

    else:
        cookieData = cookieCart(request)
        carrito = cookieData['carrito']
        order = cookieData['order']
           
    context = {'carrito' : carrito, 'products' : products, 'order': order}

    return render(request, 'base/home.html', context)



def checkOut(request):
    if request.user.is_authenticated:
        client = request.user.client
        order, create = Order.objects.get_or_create(client = client, complete=False)
        carrito = order.orderitems_set.all()
    else:
        cookieData = cookieCart(request)
        carrito = cookieData['carrito']
        order = cookieData['order']

    context = {'carrito' : carrito, 'order': order}

    return render(request, 'base/checkout.html', context)


def login_user(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password )
        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'base/login-regis.html', {'page' : page})

def register_user(request):
    form = ClientCreation()
    if request.method == 'POST':
        form = ClientCreation(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Client.objects.create(
                user = user,
                name = user.username,
                email = user.email
            )
            return redirect('home')

    return render (request, 'base/login-regis.html', {'form' : form})

def logout_user(request):
    logout(request)
    return redirect('home')

@csrf_exempt
def update_order(request):
    print(request.method)
    pk = request.POST.get('product')
    type = request.POST.get('action')
    print(pk)
    print(type)
    client = Client.objects.get(user = request.user)
    product = Product.objects.get(id = pk)
    order, created = Order.objects.get_or_create(client = client, complete = False)

    order_items, created = orderItems.objects.get_or_create(order = order, product = product) 

    if type == 'plus':
        order_items.quantify += 1
    elif type == 'less':
        if order_items.quantify < 2:
            order_items.quantify += 0
        else:  
            order_items.quantify -= 1
    order_items.save()

    dic = {}
    dic['id'] = pk
    dic['items'] = order.total_cart_items
    dic['items_quantity'] = order_items.quantify
    dic['total'] = order.total_cart
    dic['product_total'] = order_items.total_price

    dic['created'] = created
    dic['newProduct'] = order_items.product.name
    dic['newProduct_image'] = str(order_items.product.image)
    return HttpResponse(json.dumps(dic), content_type = "application/json")



def eliminateItem(request):
    if request.user.is_authenticated:
        id = request.GET.get('id')
        client = request.user.client
        product = Product.objects.get(id = id)
        order = Order.objects.get(client = client, complete = False)
        order_items = orderItems.objects.get(order = order, product = product)
        order_items.delete() 
        dic = {}
        dic['total_items'] = order.total_cart_items
        dic['id'] = id
        dic['total'] = order.total_cart
    else:
        return HttpResponse('listorti', content_type = 'application/json')

    return HttpResponse(json.dumps(dic), content_type= 'application/json')


@csrf_exempt
def orderEnded(request):
    if request.user.is_authenticated:
        transaction_id = datetime.datetime.now().timestamp()
        client = request.user.client
        order, created = Order.objects.get_or_create(client = client, complete = False)

        order.complete = True
        order.transaction_id = transaction_id
        order.save()
        ClientAddres.objects.create(
            client = client,
            order = order,
            address = request.POST['address'],
            city = request.POST['city'],
            zipcode = request.POST['zip'],
        )
    else:
        client, created = Client.objects.get_or_create(
            name = request.POST['client'],
            email = request.POST['email'],
        )
        order, created = Order.objects.get_or_create(client = client, complete = False)
        order.complete = True
        order.transaction_id = datetime.datetime.now().timestamp()
        order.save()

        ClientAddres.objects.create(
            client = client,
            order = order,
            address = request.POST['address'],
            city = request.POST['city'],
            zipcode = request.POST['zip'],
        )

        cookieData = cookieCart(request)
        items = cookieData['carrito']
        for item in items:
            product = Product.objects.get(id = item['product']['id'])
            print('------------------------------------------------------LA REPUTA MADRE QUE RE REMIL PARIO ---------------------------------')
            
            jose = orderItems.objects.create(
                product = product,
                order = order,
                quantify = item['quantify'],
            )
            print(jose)


    return JsonResponse('Enviado', safe=False)