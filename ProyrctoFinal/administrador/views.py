
import json
from django.http import JsonResponse
from django.contrib import messages
from .models import User, Encuesta, Pregunta, Respuesta, Respuesta_correcta, RespuestaUsuario
from django.shortcuts import render, redirect
from django.http import JsonResponse
# Create your views here.
def main(request):
    return render(request,'admin_html/menu.html')
def configuracion(request):
    return render(request,'admin_html/configuracion.html')
def resultados(request):
    encuestas = Encuesta.objects.all()
    datos = []

    for encuesta in encuestas:
        encuesta_data = {
            "titulo": encuesta.titulo,
            "Resultados": [],
            "Usuarios": []
        }

        verificaciones = RespuestaUsuario.objects.filter(encuesta_id=encuesta.id)
        usuarios = User.objects.filter(id__in=verificaciones.values_list("usuario_id", flat=True))

        for usuario in usuarios:
            verificacion = verificaciones.filter(usuario_id=usuario.id).first()
            if verificacion:
                arreglo = list(str(verificacion.aciertos))
                aux_usuario = usuario.email
                n = len(arreglo)
                for i in range(n - 1):
                    for j in range(0, n - i - 1):
                        if arreglo[j] < arreglo[j + 1]:
                            arreglo[j], arreglo[j + 1] = arreglo[j + 1], arreglo[j]
                            aux_usuario[j], aux_usuario[j + 1] = aux_usuario[j + 1], aux_usuario[j]
                encuesta_data['Resultados'].append(arreglo)
                encuesta_data['Usuarios'].append(aux_usuario)

        datos.append(encuesta_data)

    return render(request,'admin_html/resultados.html', {'datos': datos})
def eliminar_encuesta(request):
    if request.method == 'POST':
        encuesta = request.POST.get('encuesta')
        try:
            encuesta_ = Encuesta.objects.get(titulo=encuesta)
            encuesta_.delete()
            messages.success(request, 'Usuario eliminado correctamente.')
        except User.DoesNotExist:
            messages.error(request, 'No se encontró el usuario.')
    return render(request,'admin_html/eliminar_encuesta.html')

def eliminar_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user.email != "admin@gmail.com":
                user.delete()
                messages.success(request, 'Usuario eliminado correctamente.')
        except User.DoesNotExist:
            messages.error(request, 'No se encontró el usuario.')
    return render(request,'admin_html/eliminar_user.html')

def cambiar_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password_ = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user.password=password_;
            user.save()
            messages.success(request, 'Usuario cambio de password correctamente.')
        except User.DoesNotExist:
            messages.error(request, 'No se encontró el usuario.')
    return render(request,'admin_html/cambiar_password.html')

def guardar_respuestas(request):
    print("ty------------")
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)  # Analizar los datos JSON enviados desde el cliente
            # Realizar cualquier procesamiento adicional de los datos aquí
            # Guardar las preguntas y respuestas en tu base de datos

           # guardado de encuesta con relacion a  usuario; ya se probo
            try:
                encuesta=Encuesta.objects.get(titulo=datos['titulo'])
                mensaje="Ese nombre de encuesta ya a sido utilizado"
                return redirect( "mostrar_alert")
            except Encuesta.DoesNotExist:
                encuesta = Encuesta(titulo=datos['titulo'])
                encuesta.save()
                for usuario in datos['usuarios']:
                    try:
                        user=User.objects.get(email=usuario)
                    except User.DoesNotExist:
                        print(usuario)
                # guardado de pregunta con relacion a encuesta; ya se probo
                #encuesta = Encuesta.objects.get(titulo=datos['titulo'])  # Supongamos que queremos asociar las preguntas a la encuesta con ID 1
                for i,pregunta in enumerate(datos['preguntas']):
                    preg = Pregunta(encuesta_id=encuesta.id, texto=pregunta['texto'])
                    preg.save()
                    respuestas = datos['preguntas'][i]['respuestas']
                    for j,respuesta in enumerate(respuestas):
                        checks = datos['preguntas'][i]['checks']
                        check=Respuesta_correcta(texto=str(checks[j]),Encuesta_id=encuesta.id)
                        check.save()
                        res=Respuesta(pregunta_id=preg.id, texto=respuesta,Respuesta_correcta_id=check.id,encuesta_id=encuesta.id)
                        res.save()
                for usuario in datos['usuarios']:
                    try:
                        user = User.objects.get(email=usuario)
                        if not RespuestaUsuario.objects.filter(usuario=user.id, encuesta=encuesta.id).exists():
                            respuesta_usuario = RespuestaUsuario.objects.create(usuario_id=user.id, encuesta_id=encuesta.id,
                                                                                aciertos=0)  # Crea la instancia sin el valor de aciertos
                            respuesta_usuario.save()
                            encuesta.user.add(user.id)
                            print("ty")
                    except User.DoesNotExist:
                        print("")

            return JsonResponse({'mensaje': 'Encuesta recibida correctamente.'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON no válido.'}, status=400)

    # Si la solicitud no es POST, devolver un error
    return JsonResponse({'error': 'Método no permitido.'}, status=405)


