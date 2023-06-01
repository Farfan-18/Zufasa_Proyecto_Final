from django.shortcuts import render, redirect
from administrador.models import Encuesta, Pregunta, Respuesta, User, Respuesta_correcta, RespuestaUsuario


#from user.models import Aciertos, User_respuestas
# Create your views here.
def encuesta(request, id):
    encuestas = Encuesta.objects.all()
    datos = []

    for encuesta in encuestas:
        try:
            verificacion = RespuestaUsuario.objects.get(usuario_id=id,encuesta_id=encuesta.id)
            if not verificacion.realizado:
                if encuesta.user.filter(id=id).exists():
                    encuesta_data = {
                        "titulo": encuesta.titulo,
                        "preguntas": []
                    }
                    preguntas = Pregunta.objects.filter(encuesta=encuesta)
                    for pregunta in preguntas:
                        pregunta_data = {
                            "texto": pregunta.texto,
                            "respuestas": []
                        }
                        respuestas = Respuesta.objects.filter(pregunta=pregunta)
                        for respuesta in respuestas:
                            respuesta_ = {
                                "texto":respuesta.texto,
                                "id":respuesta.id
                            }
                            pregunta_data['respuestas'].append(respuesta_)
                        encuesta_data['preguntas'].append(pregunta_data)
                    datos.append(encuesta_data)
        except RespuestaUsuario.DoesNotExist:
            print("")
    return render(request, 'usuario_html/encuesta.html', {'datos': datos})
def guardar_encuesta(request,id):
    if request.method == 'POST':

        encuestas = Encuesta.objects.all()
        for encuesta in encuestas:
            encuestas_filtradas = encuesta.user.filter(id=id)
            preguntas = Pregunta.objects.filter(encuesta=encuesta)
            aux_=[]
            for pregunta in preguntas:
                respuestas_seleccionadas = request.POST.getlist('respuestas_'+encuesta.titulo+"_"+pregunta.texto)
                aux_.append(respuestas_seleccionadas)

            if encuesta.user.filter(id=id).exists():
                aux = RespuestaUsuario.objects.get(usuario_id=id, encuesta_id=encuesta.id)
                if not(aux.realizado):
                    preguntas = Pregunta.objects.filter(encuesta=encuesta)
                    for res_id, pregunta in zip(aux_, preguntas):
                        resp_user = Respuesta.objects.get(id=res_id[0]);
                        resp_user.user.add(id)
                        resp_user.save()

                    # Filtra las respuestas relacionadas con el usuario y obtén la ID de cada respuesta
                    ids_respuestas = Respuesta.objects.filter(user=id,encuesta_id= encuesta.id).values_list('id', flat=True)
                    # Itera sobre las IDs de las respuestas encontradas

                    cont=0;
                    for id_respuesta in ids_respuestas:
                    # Haz lo que necesites con la ID de la respuesta
                        respuesta=Respuesta.objects.get(id=id_respuesta,encuesta_id=encuesta.id)
                        if respuesta.Respuesta_correcta.texto == "True":
                            cont=cont+1
                            try:
                                respuesta_usuario = RespuestaUsuario.objects.get(usuario_id=id, encuesta_id=encuesta.id)  # Crea la instancia sin el valor de aciertos
                                respuesta_usuario.aciertos=cont
                                respuesta_usuario.realizado=True
                                respuesta_usuario.save()
                            except RespuestaUsuario.DoesNotExist:
                                print("Aun no contesta la encuesta: "+encuesta.titulo)
                        else:
                            respuesta_usuario = RespuestaUsuario.objects.get(usuario_id=id,
                                                                             encuesta_id=encuesta.id)
                            respuesta_usuario.realizado = True
                            respuesta_usuario.save()
    return redirect('../encuesta/'+str(id))