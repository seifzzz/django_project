

import decimal
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Product, Cart, Cart_items, Order, Order_items
from .serializers import (
    RegisterSerializer, UserSerializer,
    ProductSerializer, CartSerializer,
    CartItemSerializer,
    OrderSerializer
    )


# Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        Cart.objects.create(user=user, total_price=0.0, quantity=0)
        return Response({
                "user": UserSerializer(user,
                                       context=self.
                                       get_serializer_context()).data,
                "message": "User Created Successfully.  "
                           "Now perform Login to get your token",
                        })


class ProductApi(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, name=None):
        if name:
            item = Product.objects.get(name=name)
            serializer = ProductSerializer(item)
            return Response({"status": "success", "data": serializer.data},
                            status=status.HTTP_200_OK)

        items = Product.objects.all().order_by('price')
        serializer = ProductSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data},
                        status=status.HTTP_200_OK)


def update_quantity_price(cart, cart_items):
    len_items = len(cart_items)
    quantity = 0
    total_price = 0

    for i in range(len_items):
        quantity += cart_items[i].quantity
        product = Product.objects.get(id=cart_items[i].product_id)
        total_price += (decimal.Decimal
                        (cart_items[i].quantity) * product.price)

    cart.total_price = total_price
    cart.quantity = quantity


class CartApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        cart = Cart.objects.get(user_id=user.id)
        cart1 = Cart.objects.filter(user_id=user.id)
        items = Cart_items.objects.filter(cart_id=cart.id)
        serializer = CartSerializer(cart1, many=True)
        serializer2 = CartItemSerializer(items, many=True)

        return Response({"status": "success", "Cart": serializer.data,
                        "Cart item ": serializer2.data},
                        status=status.HTTP_200_OK)

    def post(self, request):

        user = request.user
        cart = Cart.objects.get(user_id=user.id)
        serializer = CartItemSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            cart_items = Cart_items.objects.filter(cart_id=cart.id)
            update_quantity_price(cart, cart_items)

            cart.save()

            return Response({"status": "success", "data": serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class OrderApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        order1 = Order.objects.filter(user_id=user.id)
        serializer = OrderSerializer(order1, many=True)

        return Response({"status": "success", "Order": serializer.data},
                        status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        cart = Cart.objects.get(user_id=user.id)

        if cart is None:
            return Response({"status": "success" "Cart is empty"},
                            status=status.HTTP_200_OK)

        order = Order.objects.create(
            user=user,
            quantity=cart.quantity,
            total_price=cart.total_price)

        cart_items = Cart_items.objects.filter(cart_id=cart.id)
        order1 = Order.objects.filter(pk=order.id)

        for i in range(len(cart_items)):
            Order_items.objects.create(
                order=order,
                product=cart_items[i].product,
                quantity=cart_items[i].quantity)

        cart.delete()
        cart_items.delete()
        serializer = OrderSerializer(order1, many=True)
        return Response(
            {"status": "success", "Order is Created": serializer.data},
            status=status.HTTP_200_OK)
