from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.urls import reverse

import subprocess

from django.db import connection
from administrador.models import User
#sirve para llamar la pagina html
# Create your views here.
def main (request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST['email'],password=request.POST['password'])
            if user.email == 'admin@gmail.com':
                return redirect('menu')
            else:
                return redirect('../encuesta/'+str(user.id))

        except User.DoesNotExist :
            return render(request, 'login_html/index.html')
    return render(request, 'login_html/index.html')

def crear_user (request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password2']:
            try:
                user=User.objects.get(email=request.POST['email'])
                return HttpResponse("usuario existente")
            except User.DoesNotExist :
                user = User(email=request.POST['email'], password=request.POST['password'])
                user.save()
                return redirect('../login/')
        else:
            return HttpResponse("error Password")
    return render(request, 'login_html/crear_user.html')

def recuperar_password (request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST['email'])
            password_r=user.password
            email_destino=request.POST['email']
            asunto = 'Recuperaste tu password :)'
            mensaje = 'Tu contraseña es: '+password_r
            remitente = '1sistemasequipo@gmail.com'
            recipient_list= [email_destino]
            M = EmailMessage(asunto,mensaje,remitente,recipient_list)
            #send_mail(asunto, mensaje, remitente, recipient_list)
            try:
                M.send()
                print("ty")
                return redirect("login")
            except:
                print("no")
                return redirect("recuperar_password")
            return render (request, 'login_html/index.html')
        except User.DoesNotExist:
            print( 'Error.')
            return render(request, 'login_html/recuperar_password.html')
    return render(request, 'login_html/recuperar_password.html')

