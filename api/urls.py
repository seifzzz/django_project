

from rest_framework_simplejwt import views as jwt_views
from django.urls import path
from api.views import RegisterApi, ProductApi, CartApi, OrderApi

urlpatterns = [

   path('api/token/',
        jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(),
        name='token_refresh'),
   path('register', RegisterApi.as_view()),
   path('product/', ProductApi.as_view()),
   path('product/<str:name>', ProductApi.as_view()),
   path('cart/', CartApi.as_view()),
   path('order/', OrderApi.as_view())

   ]
