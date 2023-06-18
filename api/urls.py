from rest_framework_simplejwt import views as jwt_views
from django.urls import path
from api.views import RegisterApi, Add_Product, \
    All_Product, Show_Cart, \
    Add_item_Cart, \
    OrderApi, \
    Make_OrderApi
from drf_spectacular.views import SpectacularAPIView, \
    SpectacularSwaggerView

urlpatterns = [

   path('login/',
        jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(),
        name='token_refresh'),
   path('register', RegisterApi.as_view()),

   path('product/add', Add_Product.as_view()),
   path('product/<str:name>', All_Product.as_view()),
   path('product/all', All_Product.as_view()),

   path('cart/all_items', Show_Cart.as_view()),
   path('cart/add_item', Add_item_Cart.as_view()),

   path('order/show/', OrderApi.as_view()),
   path('order/make/', Make_OrderApi.as_view()),

   path("schema/", SpectacularAPIView.as_view(), name="schema"),
   path("docs/", SpectacularSwaggerView.
        as_view(template_name="swagger_ui.html",
                url_name="schema"),
        name="swagger-ui")
   ]
