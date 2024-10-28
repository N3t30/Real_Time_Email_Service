from django.urls import path
from messaging.views import send_message
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.views import LogoutView
from .views import (
    home,
    index,
    register_view,
    login_view, 
    painel,   
)


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('', home, name='home'),
    path('index/', index, name='index'),
    path('send/', send_message, name='send_message'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('painel/', painel, name='painel'),
    # path('messaging/', include('messaging.urls')),
]
