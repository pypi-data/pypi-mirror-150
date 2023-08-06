from django.urls import path, include
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', include('courses.urls')),
    path('<str:lang>/', views.home, name='home'),
]