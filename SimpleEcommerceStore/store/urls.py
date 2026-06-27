from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),

    path("products/", views.products, name="products"),

    path("product/<int:id>/", views.product_detail, name="product_detail"),

    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.cart, name='cart'),

    path("remove-from-cart/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),

    path("increase/<int:item_id>/", views.increase_quantity, name="increase_quantity"),
    
    path("decrease/<int:item_id>/", views.decrease_quantity, name="decrease_quantity"),

    path("login/", views.login_user, name="login"),

    path("register/", views.register_user, name="register"),

    path("logout/", views.logout_user, name="logout"),

    path("checkout/", views.checkout, name="checkout"),

    path("orders/", views.orders, name="orders"),
]