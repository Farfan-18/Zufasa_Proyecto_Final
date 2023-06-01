from django.urls import path
from . import views

urlpatterns =[
    path('menu/', views.main,name='menu'),
    path('configuracion/', views.configuracion,name='configuracion'),
    path('resultados/', views.resultados,name='resultados'),
    path('eliminar_usuario/', views.eliminar_usuario,name='eliminar_usuario'),
    path('guardar_respuestas/', views.guardar_respuestas,name='guardar_respuestas'),
    path('cambiar_password/', views.cambiar_password,name='cambiar_password'),
    path('eliminar_encuesta/', views.eliminar_encuesta,name='eliminar_encuesta'),
]