from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    
    path('', views.home, name="home"), 

    path('contact_point_methods/', views.contact_point_methods, name="contact_point_methods"),
    path('contact/<int:pk>/', views.contact, name="contact"),
    path('contact/create/', views.create_contact, name="create_contact"),
    path('contact/settings/<str:pk>/', views.contact_settings, name="contact_settings"),

    path('create_contact_point/<str:pk>/', views.create_contact_point, name="create_contact_point"),
    path('update_contact_point/<str:pk>/', views.update_contact_point, name="update_contact_point"),
    path('delete_contact_point/<str:pk>/', views.delete_contact_point, name="delete_contact_point"),

    path('update_contact_point_methods/', views.create_contact_point_methods, name="update_contact_point_methods"),
    path('update_contact_tags/', views.create_contact_tags, name="update_contact_tags"),
]