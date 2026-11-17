
from django.urls import path
from . import views

urlpatterns = [
    # Login page appears first
    path('', views.user_login, name='login'),
    path('login/', views.user_login, name='login_page'),

    # Register
    path('register/', views.register, name='register'),

    #Dashboard
    path('home/', views.home, name='home'),

    # User CRUD
    path('read/', views.read, name='read'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),

    # Logout
    path('logout/', views.user_logout, name='logout'),
]
