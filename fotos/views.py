from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from usuarios.models import Usuario
from .models import Post, ComentarioPost, Like, Notificaciones

def home(request):
    user_followed = Usuario.objects.filter(followers=request.user)
    posts = Post.objects.filter(usuario__in=user_followed)
    results = []
    for pub in posts:
        results.append(pub)
        if Like.objects.filter(post=pub, user=request.user).exists():
            pub.is_liked = True
    contexto = {
        'posts': results
    }
    return render(request, 'fotos/feed.html', contexto)

def post_comments(request, id):
    post = Post.objects.get(id=id)
    contexto = {'post': post}
    return render(request, 'fotos/comentarios.html', contexto)

def post_form(request):
    return render(request, 'fotos/post_form.html')

def subir_foto(request):
    salida = {}
    if request.method == 'POST' and request.is_ajax():
        imagen_ = request.FILES.get('post')
        pie_foto = request.POST.get('pie')
        user = Usuario.objects.get(id=request.user.id)
        fecha_ = timezone.now()

        if imagen_ and pie_foto:
            post = Post.objects.create(
                imagen=imagen_,
                fecha=fecha_,
                pie=pie_foto,
                usuario=user,
            )
            post.save()
            salida = {'success': True, 'msj': 'Post subido correctamente'}
        else:
            salida = {'error': True, 'msj': 'Por favor llena todos los campos'}
    return HttpResponse(JsonResponse(salida))

def pub_detalles(request, id):
    is_liked = False
    is_saved = False
    pub = Post.objects.get(id=id)
    num_likes = Like.objects.filter(post=pub).count()
    if Like.objects.filter(post=pub, user=request.user).exists():
        is_liked = True
    if pub.guardar.filter(id=request.user.id).exists():
        is_saved = True
    comentarios = ComentarioPost.objects.filter(post_id=pub.id)
    contexto = {
        'foto': pub,
        'comentarios': comentarios,
        'is_liked': is_liked,
        'is_saved': is_saved,
        'num_likes': num_likes
    }
    return render(request, 'fotos/pub_detalles.html', contexto)

def likear(request, id):
    salida = {}
    foto = Post.objects.get(id=id)
    second_user = foto.usuario
    current_user = request.user
    if request.method == 'POST' and request.is_ajax():
        if Like.objects.filter(post=foto, user=current_user).exists():
            like_object = Like.objects.filter(post=foto, user=current_user)
            like_object.delete()
            salida = {'deleted': True}
        else:
            date = timezone.now()
            like_object = Like.objects.create(
                post=foto,
                user=current_user,
                fecha=date
            )
            like_object.save()
            texto_ = 'le ha dado like tu foto'
            ntc = Notificaciones.objects.create(
                post=foto,
                f_user=current_user,
                fecha=date,
                s_user=second_user,
                texto = texto_
            )
            ntc.save()
            salida = {'liked': True}
    return HttpResponse(JsonResponse(salida))

def guardar_post(request, id):
    salida = {}
    foto = Post.objects.get(id=id)
    current_user = request.user
    if request.method == 'POST' and request.is_ajax():
        if foto.guardar.filter(id=current_user.id).exists():
            foto.guardar.remove(current_user)
            salida = {'removed': True}
        else:
            foto.guardar.add(current_user)
            salida = {'saved': True}
    return HttpResponse(JsonResponse(salida))

def comentar(request, id):
    salida = {}
    if request.method == 'POST' and request.is_ajax():
        pub = Post.objects.get(id=id)
        second_user = pub.usuario
        comentario = request.POST.get('comentario')
        date = timezone.now()
        if comentario:
            nuevo_comentario = ComentarioPost.objects.create(
                post=pub,
                fecha=date,
                user=request.user,
                texto=comentario
            )
            nuevo_comentario.save()
            texto_ = 'ha comentado tu foto'
            ntc = Notificaciones.objects.create(
                post=pub,
                f_user=request.user,
                fecha=date,
                s_user=second_user,
                texto=texto_
            )
            ntc.save()
            comentario_ajax = []
            comentario_info = {}
            name_ = request.user.username
            comentario_info['texto'] = nuevo_comentario.texto
            comentario_info['fecha'] = nuevo_comentario.fecha
            comentario_info['user'] = name_
            comentario_ajax.append(comentario_info)
            salida = {'success': True, 'info': comentario_ajax}
        else:
            salida = {'error': True}
    return HttpResponse(JsonResponse(salida))

def get_likes(request, id):
    pub = Post.objects.get(id=id)
    likes = Like.objects.filter(post=pub)
    contexto = {'likes': likes}
    return render(request, 'fotos/modal.html', contexto)

def get_saved(request):
    posts = Post.objects.filter(guardar=request.user)
    context = {'posts': posts}
    return render(request, 'fotos/guardados.html', context)

def busqueda(request):
    return render(request, 'fotos/buscador.html')

def notificaciones(request):
    nts = Notificaciones.objects.filter(s_user=request.user)
    contexto = {'notificaciones': nts}
    return render(request, 'fotos/notificaciones.html', contexto)