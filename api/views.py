import decimal
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt import authentication
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


class Add_Product(generics.GenericAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK
                )
        else:
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
                )


class All_Product(generics.GenericAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, name=None):
        if name:
            item = Product.objects.filter(name=name)
            if len(item) == 0:
                return Response({"status": "success",
                                 "Message":
                                     "there is no product with this name "},
                                status=status.HTTP_200_OK)

            serializer = ProductSerializer(item[0])
            return Response({"status": "success", "data": serializer.data},
                            status=status.HTTP_200_OK)

        items = Product.objects.all().order_by('price')

        if len(items) == 0:
            return Response(
                {"status": "success",
                 "Message": "there no available products"},
                status=status.HTTP_200_OK)

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


class Show_Cart(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    serializer_class = CartItemSerializer

    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user_id=user.id)
        items = Cart_items.objects.filter(cart_id=cart[0].id)

        if len(items) == 0:
            return Response({"status": "success",
                             "Message": "Your Cart is empty"},
                            status=status.HTTP_200_OK)

        serializer = CartSerializer(cart, many=True)
        serializer2 = CartItemSerializer(items, many=True)

        return Response({"status": "success", "Cart": serializer.data,
                        "Cart item ": serializer2.data},
                        status=status.HTTP_200_OK)


class Add_item_Cart(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    serializer_class = CartItemSerializer

    def post(self, request):

        user = request.user
        cart = Cart.objects.get(user_id=user.id)
        serializer = CartItemSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            cart_items = Cart_items.objects.filter(cart_id=cart.id)
            update_quantity_price(cart, cart_items)

            cart.save()

            return Response({"status": "success",
                             "Message": "Item added to cart"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class OrderApi(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.JWTAuthentication]
    serializer_class = OrderSerializer

    def get(self, request):
        user = request.user

        order1 = Order.objects.filter(user_id=user.id)
        if len(order1) == 0:
            return Response(
                {"status": "success", "Message": "You didn't make any order"},
                status=status.HTTP_200_OK
                )
        serializer = OrderSerializer(order1, many=True)

        return Response({"status": "success", "Order": serializer.data},
                        status=status.HTTP_200_OK)


class Make_OrderApi(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.JWTAuthentication]
    serializer_class = OrderSerializer

    def get(self, request):
        user = request.user
        cart = Cart.objects.get(user_id=user.id)

        if cart.quantity == 0:
            return Response(
                {"status": "success", "Message": "Cart is empty"},
                status=status.HTTP_200_OK
                )

        order = Order.objects.create(
            user=user,
            quantity=cart.quantity,
            total_price=cart.total_price
            )

        cart_items = Cart_items.objects.filter(cart_id=cart.id)
        order1 = Order.objects.filter(pk=order.id)

        for i in range(len(cart_items)):
            Order_items.objects.create(
                order=order,
                product=cart_items[i].product,
                quantity=cart_items[i].quantity
                )

        cart.quantity = 0
        cart.total_price = 0
        cart.save()

        cart_items.delete()
        serializer = OrderSerializer(order1, many=True)
        return Response(
            {"status": "success", "Order is Created": serializer.data},
            status=status.HTTP_200_OK
            )
