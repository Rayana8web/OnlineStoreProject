from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

from django.urls import path, include
#start
from .views import estate_detail_view, estate_like_view, create_comment_view

urlpatterns = [
    path ('', views.index_view),
    path('', views.index_view, name='index'),
    path('estate/<int:pk>/', views.estate_detail_view, name='estate_detail'),
    path('login/', auth_views.LoginView.as_view(), name='login'),

    path('estate_list/', views.estate_list_view, name='estate_list'),
    path('estate/<int:estate_id>/comment/', create_comment_view, name='comment_create'),
    path('estate/<int:estate_id>/like/', estate_like_view, name='estate_like'),
]

