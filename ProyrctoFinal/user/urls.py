from django.urls import path,include
from . import views
urlpatterns =[
    path('encuesta/<int:id>', views.encuesta, name="encuesta"),
    path('guardar_encuesta/<str:id>', views.guardar_encuesta, name='guardar_encuesta'),

]