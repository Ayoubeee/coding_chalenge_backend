from django.urls import path
from .views import SignUp,SignIn,is_login,list_shops,like_shop,remove_shop,list_prefer_shops
urlpatterns = [
    path('SignUp/', SignUp),
    path('SignIn/', SignIn),
    path('is_login/', is_login),
    path('list_shops/', list_shops),
    path('like_shop/', like_shop),
    path('remove_shop/', remove_shop),
    path('list_prefer_shops/', list_prefer_shops),
]
