from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_func, name='index'),
    path('login/', views.login_func, name='login'),
    path('app1/', views.app1_func, name='app1'),
    path('app2/', views.app2_func, name='app2'),
    path('app3/', views.app3_func, name='app3')
]