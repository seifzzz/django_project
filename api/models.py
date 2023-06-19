from django.db import models
from django.contrib.auth.models import User


# Product class has name and price
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=8, decimal_places=2
        )


# Cart Class  has total price , total quantity and user
# Every user has one cart only
class Cart(models.Model):
    total_price = models.DecimalField(
        max_digits=8, decimal_places=2
        )
    quantity = models.IntegerField()
    user = models.OneToOneField(
        User, related_name="carts", on_delete=models.CASCADE
        )


# every cart has many cart items , every cart item has product(product id) , quantity and cart(cart_id)
class Cart_items(models.Model):
    product = models.ForeignKey(
        Product, related_name='items', on_delete=models.CASCADE
        )
    cart = models.ForeignKey(
        Cart, related_name='items', on_delete=models.CASCADE
        )
    quantity = models.IntegerField()


# order class to user make orders and stored on it.
class Order(models.Model):
    user = models.ForeignKey(
        User, related_name="order", on_delete=models.CASCADE
        )
    total_price = models.DecimalField(
        max_digits=8, decimal_places=2
        )
    quantity = models.IntegerField()


# every order has items
class Order_items(models.Model):
    product = models.ForeignKey(
        Product, related_name='order_items', on_delete=models.CASCADE
        )
    order = models.ForeignKey(
        Order, related_name='order_items', on_delete=models.CASCADE
        )
    quantity = models.IntegerField()
