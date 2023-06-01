from django.db import models
# Create your models here.


class User(models.Model):#--
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=100)

class Encuesta(models.Model):#--
    titulo = models.CharField(max_length=100)
    user = models.ManyToManyField(User, through='RespuestaUsuario')

class Pregunta(models.Model):
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    texto = models.TextField()

class Respuesta_correcta(models.Model):#--
    texto = models.TextField()
    Encuesta= models.ForeignKey(Encuesta, on_delete=models.CASCADE)

class Respuesta(models.Model):#<---------------
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    Respuesta_correcta = models.ForeignKey(Respuesta_correcta, on_delete=models.CASCADE)
    encuesta=  models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    user = models.ManyToManyField(User)
    texto = models.TextField()


class RespuestaUsuario(models.Model):#--------
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    aciertos = models.IntegerField()
    realizado = models.BooleanField(default=False)
    class Meta:
        unique_together = ('encuesta', 'usuario')
