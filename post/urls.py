from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('delete_post/<int:post_id>', views.delete_post, name='delete_post'),
    path('create_post/', views.create_post, name='create_post'),
    path('likes_post/<int:post_id>', views.likes_post, name='likes_post'),
]