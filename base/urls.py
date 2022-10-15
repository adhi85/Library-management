from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login_user'),
    path('register', views.register_user, name='register_user'),
    path("logout", views.logout_user, name="logout_user"),

    path('mycart', views.mycart, name='mycart'),
    path('confirm/<str:pk>', views.confirm, name='confirm'),
    path('return/<str:pk>', views.return_book, name='return_book'),

    path('allbooks', views.allbooks, name='allbooks'),
]
