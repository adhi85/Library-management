from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign_in_admin/', views.sign_in_admin , name='sign_in_admin'),
    path('login/', views.login_user, name='login_user'),
    path('register', views.register_user, name='register_user'),
    path("logout", views.logout_user, name="logout_user"),

    path('mycart', views.mycart, name='mycart'),
    path('confirm/<str:pk>', views.confirm, name='confirm'),
    path('return/<str:pk>', views.return_book, name='return_book'),

    path('allbooks', views.allbooks, name='allbooks'),
    path('addbook', views.addBook, name='addBook'),
    path('deletebooks', views.deletebook, name='deletebook'),
    path('deletebook<str:pk>', views.delete, name='deletebook'),

    path('list/', views.list, name='list'),
]
