from django.urls import path,include
from . import views
urlpatterns =[
    path('login/', views.main, name="login"),
    path('recuperar_password/', views.recuperar_password,name="recuperar_password"),
    path('crear_user/', views.crear_user,name="crear_user"),
]