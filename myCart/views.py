from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Product, CartItem, UserDetails
from django.contrib.auth.decorators import login_required


# Create your views here.
def login_user(request):
    return render(request, 'login.html')


def signup_user(request):
    return render(request, 'signup.html')


def home(request):
    all_products = []
    categories = Product.objects.values('category', 'id')
    cats = {item['category'] for item in categories}
    for cat in cats:
        products = Product.objects.filter(category=cat)
        all_products.append(products)
    context = {'products': all_products}
    return render(request, 'home.html', context)


def handleSignup(request):
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        my_user = User.objects.create_user(username, email, password)
        my_user.first_name = first_name
        my_user.last_name = last_name
        my_user.save()

        messages.success(request, 'Signed Up Successfully')
        return redirect('home')


def handleLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None and 'pk' in request.session:
            login(request, user)
            messages.success(request, 'Successfully Logged In')
            addToCart(request)
            return redirect('home')
        if user is not None and 'pk' not in request.session:
            login(request, user)
            messages.success(request, 'Successfully Logged In')
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')
            return redirect('login')


def handleLogout(request):
    logout(request)
    messages.success(request, 'You have logged out')
    return redirect('home')


@login_required(login_url='login')
def addToCart(request):
    if request.method == 'POST' and 'pk' not in request.session:
        pk = request.POST.get('hidden1')
        product = Product.objects.get(id=pk)
        if request.user.is_authenticated:
            user = request.user
            queryset = CartItem.objects.filter(user=user, product=product)
            if queryset.exists():
                pass
                return redirect('home')
            else:
                cart = CartItem(user=user, product=product)
                cart.save()
                return redirect('home')
    elif 'pk' in request.session:
        user = request.user
        print(user)
        pk = request.session['pk']
        del request.session['pk']
        product = Product.objects.get(id=pk)
        queryset = CartItem.objects.filter(user=user, product=product)
        if queryset.exists():
            pass
            return redirect('home')
        else:
            cart = CartItem(user=user, product=product)
            cart.save()
            return redirect('home')


@login_required(login_url='login')
def viewCart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = CartItem.objects.filter(user=user)
        print(cart)
        sum_item = []
        cart_total = 0
        for i in cart:
            sum_item.append(i.get_total_price())
        for addn in sum_item:
            cart_total = cart_total + addn
        if cart.exists():
            content = {'cart': cart, 'cart_total': cart_total}
            return render(request, 'mycart.html', content)
        else:
            messages.error(request, 'Your Cart is empty')
            return redirect('home')


def setSession(request):
    if request.method == 'POST':
        pk = request.POST.get('hidden2')
        request.session['pk'] = pk
        messages.error(request, 'Login to access cart')
        return redirect('login')


@login_required(login_url='login')
def add_item_by_one(request):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        pk = request.POST.get('hidden')
        cart = CartItem.objects.get(id=pk)
        cart.quantity += 1
        cart.save()
        return redirect('viewCart')


@login_required(login_url='login')
def reduce_item_by_one(request):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity == '1':
            messages.error(request, 'Items cannot be zero you can Remove item by remove button')
            return redirect('viewCart')
        else:
            pk = request.POST.get('hidden')
            cart = CartItem.objects.get(id=pk)
            cart.quantity -= 1
            cart.save()
            return redirect('viewCart')


@login_required(login_url='login')
def removeItem(request):
    if request.method == 'POST':
        pk = request.POST.get('hiddenip')
        cart = CartItem.objects.filter(id=pk).delete()
        return redirect('viewCart')


@login_required(login_url='login')
def checkout(request):
    user = request.user
    cart = CartItem.objects.filter(user=user)
    sum_item = []
    cart_total = 0
    for i in cart:
        sum_item.append(i.get_total_price())
    for addn in sum_item:
        cart_total = cart_total + addn
    print(cart_total)
    user_details = UserDetails.objects.filter(user=user)
    if user_details:
        print('1')
        context = {'user_details': user_details, 'cart_total': cart_total}
        return render(request, 'checkout.html', context)
    else:
        print('2')
        context = {'cart_total': cart_total}
        return render(request, 'checkout.html', context)


@login_required(login_url='login')
def placeOrder(request):
    if request.method == 'POST':
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        mobile = request.POST.get('mobile')

        user = request.user
        details = UserDetails.objects.filter(user=user, address_line_1=address1, address_line_2=address2, city=city,
                                             state=state, zipcode=zipcode, mobile=mobile)
        if details:
            pass
        else:
            user_details = UserDetails(user=user, address_line_1=address1, address_line_2=address2,
                                       city=city, state=state, zipcode=zipcode, mobile=mobile)
            user_details.save()
        cart = CartItem.objects.filter(user=user).delete()
        messages.success(request, 'Your order has been placed')
        return redirect('home')
