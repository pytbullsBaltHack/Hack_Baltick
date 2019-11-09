from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='webface-home'),
    path('about/', views.about, name='webface-about'),
]
