from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CartItem, Order



def home(request):
    products = Product.objects.all()
    return render(request, "home.html", {"products": products})


def products(request):
    products = Product.objects.all()
    return render(request, "products.html", {"products": products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "product_detail.html", {"product": product})

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart_item, created = CartItem.objects.get_or_create(product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

def cart(request):
    cart_items = CartItem.objects.all()

    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total
    })

def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()

    return redirect('cart')
def increase_quantity(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


def decrease_quantity(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('home')

    return render(request, "login.html")

def register_user(request):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("login")

    return render(request, "register.html")

def logout_user(request):
    logout(request)
    return redirect("home")

from django.contrib.auth.decorators import login_required

@login_required
def checkout(request):
    cart_items = CartItem.objects.all()

    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":

        Order.objects.create(
            user=request.user,
            total_price=total
        )

        cart_items.delete()

        return render(request, "order_success.html")

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "total": total
    })

from django.contrib.auth.decorators import login_required

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, "order.html", {
        "orders": orders
    })