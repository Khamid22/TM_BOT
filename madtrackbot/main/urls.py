from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('edit_prescription/<int:prescription_id>/', views.edit_prescription, name='edit_prescription'),

]