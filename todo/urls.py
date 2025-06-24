from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('add/', views.add_todo, name='add_todo'),
    path('edit/<int:todo_id>/', views.edit_todo, name='edit_todo'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('toggle/<int:todo_id>/', views.toggle_todo, name='toggle_todo'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
