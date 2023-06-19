from rest_framework_simplejwt import views as jwt_views
from django.urls import path
from api.views import (
    RegisterApi, Add_Product,
    All_Product, Show_Cart,
    Add_item_Cart,
    OrderApi,
    Make_OrderApi, )
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView, )

urlpatterns = [
    # url for login ,
    path(
        'login/',
        jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'
        ),
    path(
        'api/token/refresh/', jwt_views.TokenRefreshView.as_view(),
        name='token_refresh'
        ),
    # url for refresh token
    path('register', RegisterApi.as_view()),

    # for adding product
    path('product/add', Add_Product.as_view()),
    # for getting product by has name
    path('product/<str:name>', All_Product.as_view()),
    # for get all products
    path('product/all', All_Product.as_view()),

    # for get user's cart and item's cart
    path('cart/all_items', Show_Cart.as_view()),
    # to add item on cart
    path('cart/add_item', Add_item_Cart.as_view()),

    # to get all orders whose user made it
    path('order/show/', OrderApi.as_view()),
    # to make order
    path('order/make/', Make_OrderApi.as_view()),

    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # swagger ui
    path(
        "docs/", SpectacularSwaggerView.
        as_view(
            template_name="swagger_ui.html",
            url_name="schema"
            ),
        name="swagger-ui"
        )
    ]
