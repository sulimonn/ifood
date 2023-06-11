import json
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.views.generic.edit import CreateView


def show_rest(request, rest_slug):
    rest = get_object_or_404(Restaurant, slug=rest_slug)
    filters = FoodFilter.objects.filter(rest=rest.id)
    if request.GET:
        menu = Menu.objects.filter(rest=rest.id, cat=request.GET['filter']).order_by('cat')
    else:
        menu = Menu.objects.filter(rest=rest.id).order_by('cat')

    context = {
        'title': rest.title,
        'menus': menu,
        'rest': rest,
        'filters': filters,
        'rest_slug': rest_slug
    }
    return render(request, 'oursite/restaurant/restaurant.html', context)


def index(request):
    rests = Restaurant.objects.all()[:4].values()
    return render(request, 'oursite/welcomepage.html', {'rests': rests, 'title': 'Главная страница'})


def add_to_cart(request):
    data = json.loads(request.body)
    food_id = int(data['foodId'])
    action = data['action']

    user = request.user
    food = Menu.objects.get(id=food_id)

    cart, create = UserCart.objects.get_or_create(food=food, user=user)

    if create is not True:
        if action == 'add':
            cart.quantity = cart.quantity + 1
        else:
            cart.quantity = cart.quantity - 1
    cart.save()

    if cart.quantity <= 0:
        cart.delete()
    return JsonResponse('item added', safe=False)


def get_cart(request):
    data = {}
    print(request.user)
    if request.body:
        data = json.loads(request.body)
    rest = data.get('rest')
    if request.user != 'AnonymousUser':
        cart = UserCart.objects.filter(user=request.user, rest_id=rest).values('id', 'food', 'food__title', 'total', 'quantity', 'rest__title')
    else:
        cart = ''
    return JsonResponse(list(cart), safe=False)


def remove_all(request):
    data = {}
    if request.body:
        data = json.loads(request.body)
    rest = data.get('rest')
    user = request.user
    if request.user != 'AnonymousUser':
        UserCart.objects.filter(user=user, rest_id=rest).delete()
    return JsonResponse('deleted', safe=False)


def successful_order(request):
    rest = request.GET.get('rest')
    cart = UserCart.objects.filter(user=request.user, rest__slug=rest)
    print(cart)
    address = request.GET.get('location')
    print(address)
    try:
        RestLocation.objects.get(loc__title=address, rest__slug=rest)
        deliv = 100
    except:
        deliv = 170

    total = 0
    amount = deliv + 15
    rest_pk = None
    for el in cart:
        total += el.food.price
        rest = el.food.rest
        rest_pk = el.food.rest.id

    amount += total

    context = {
        'deliv': deliv,
        'cart': cart,
        'serv': 15,
        'title': 'Ваш заказ на пути',
        'amount': amount,
        'total': total,
        'rest': rest,
        'rest_id': rest_pk
    }
    return render(request, 'oursite/order.html', context)


def order(request):
    userprofile = User.objects.get(username=request.user.username)
    print(userprofile.phone_number)
    if userprofile.phone_number == '' and userprofile.current_address == '':
        return JsonResponse({'error': 'User data not found'}, status=400)
    elif userprofile.phone_number is None:
        return JsonResponse({'error': 'User phone number not found'}, status=401)
    elif userprofile.current_address is None:
        return JsonResponse({'error': 'User current address not found'}, status=402)
    else:
        arr = {}
        data = {}
        if request.body:
            data = json.loads(request.body)
            arr = data['arr']
            deliv = data['delivery']
            service = data['serv']
        total = 0
        rest = ''
        for el in arr:
            cart = UserCart.objects.get(pk=el)
            rest = cart.rest
            total += cart.total

        with transaction.atomic():
            order = Order(user=request.user, rest=rest, amount=total)
            order.delivery = data['delivery']
            order.service = data['serv']
            order.save()
            for el in arr:
                cart = UserCart.objects.get(pk=el)
                orderDetail = OrderDetail(user=request.user, food=cart.food, order=order, quantity=cart.quantity,
                                          total=cart.total)
                orderDetail.save()
                cart.delete()
        delivery = None
        if data['delivery'] == 170:
            delivery = 30
        else:
            delivery = 60
        return JsonResponse({'delivery' : delivery}, safe=False)


class Register(CreateView):
    form_class = RegistrationForm
    template_name = 'oursite/logging/signup.html'
    extra_context = {
        'title': 'Регистрация'
    }

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)

        return response


class Login(LoginView):
    form_class = LoginForm
    template_name = 'oursite/logging/signin.html'
    fields = ['email', 'password']
    extra_context = {
        'title': 'Авторизация'
    }

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return '/'


def logout_user(request):
    logout(request)
    return redirect('login')


def update_data(request):
    data = json.loads(request.body)
    type = data['type']
    data = data['data']
    user = User.objects.get(username=request.user.username)
    if type == 'text':
        user.first_name = data
    elif type == 'number':
        user.phone_number = data

    response = {}
    if user.save() is None:
        if type == 'text':
            data = user.first_name
        elif type == 'number':
            data = user.phone_number
        response = {
            'status': 200,
            'data': data
        }
    else:
        response = {
            'status': 400,
            'data': 'Something went wrong'
        }
    return JsonResponse(response, safe=False)


def locations(request):
    location = Location.objects.all().values('id', 'title')
    return JsonResponse(list(location), safe=False)


def update_location(request):
    user = User.objects.get(username=request.user.username)

    try:
        data = json.loads(request.body)
        id = data['id']
        location = Location.objects.get(id=id)
        user.current_address = location
        user.save()
        status = 200
    except:
        status = 400
    response = {
        'status': status
    }
    return JsonResponse(response, safe=False)


def restaurants(request):
    loc = request.GET.get('location')
    restNearByUser = RestLocation.objects.filter(loc_id=loc)
    rests = RestLocation.objects.exclude(loc_id=loc)
    filters = Filter.objects.all()

    context = {
        'restsNearByUser': restNearByUser,
        'rests': rests,
        'location': loc,
        'filters': filters
    }

    return render(request, 'oursite/restaurants/restaurants.html', context)


def orders(request):
    user = User.objects.get(username=request.user.username)
    ordersUser = Order.objects.filter(user=user).values('id', 'user', 'rest', 'amount', 'orderDate')

    return JsonResponse(list(ordersUser), safe=False)

