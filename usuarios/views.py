from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import check_password
from .models import Usuario
from fotos.models import Notificaciones
from fotos.models import Post
from .forms import UserForm
import re
from django.db.models import Q
from django.utils import timezone

def login_home(request):
    return render(request, 'usuarios/login.html')

def registrarse_home(request):
    return render(request, 'usuarios/registrarse.html')

def user_home(request):
    fotos = Post.objects.filter(usuario_id=request.user.id)
    contexto = {'fotos': fotos}
    return render(request, 'usuarios/user_home.html', contexto)

def user_profile(request, id):
    following = False
    user = Usuario.objects.get(id=id)
    fotos = Post.objects.filter(usuario_id=user.id)
    if user.followers.filter(id=request.user.id).exists():
        following = True
    contexto = {'usuario': user, 'fotos': fotos, 'following': following}
    return render(request, 'usuarios/user_page.html', contexto)

def registrarse(request):
    salida = {}
    if request.method == 'POST' and request.is_ajax():
        username_ = request.POST.get('username')
        nombre_ = request.POST.get('nombre')
        apellido_ = request.POST.get('apellido')
        email_ = request.POST.get('email')
        pass_ = request.POST.get('password')
        pass_confir = request.POST.get('password2')

        if username_ and nombre_ and apellido_ and email_ and pass_ and pass_confir:
            ex_regular = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"
            if re.match(ex_regular, email_):
                if len(pass_) > 6:
                    if pass_ == pass_confir:
                        if not(Usuario.objects.filter(username=username_).exists()):
                            if not(Usuario.objects.filter(email=email_).exists()):
                                user = Usuario.objects.create(
                                    username=username_,
                                    first_name=nombre_,
                                    last_name=apellido_,
                                    email=email_,
                                    password=pass_
                                )
                                user.set_password(request.POST.get('password'))
                                user.save()
                                user = authenticate(username=username_, password=pass_)
                                login(request, user)
                                salida = {'success': True, 'msj': 'Registrado'}
                            else:
                                salida = {'error': True, 'msj': 'Ese email ya esta registrado'}
                        else:
                            salida = {'error': True, 'msj': 'Ese nombre de usuario ya esta registrado'}
                    else:
                        salida = {'error': True, 'msj': 'Las contraseñas no coinciden'}
                else:
                    salida = {'error': True, 'msj': 'Por favor ingresa una contraseña mas larga'}
            else:
                salida = {'error': True, 'msj': 'Por favor ingresa un email valido'}
        else:
            salida = {'error': True, 'msj': 'Por favor llena todos los campos'}
    return HttpResponse(JsonResponse(salida))

def login_user(request):
    salida = {}
    if request.method == 'POST' and request.is_ajax():
        username_ = request.POST.get('username')
        password_ = request.POST.get('password')

        if username_ and password_:
            if Usuario.objects.filter(username=username_).exists():
                get_user = Usuario.objects.get(username=username_)
                get_pass = get_user.password
                if check_password(password_, get_pass):
                    user = authenticate(username=username_, password=password_)
                    if user is not None:
                        login(request, user)
                        salida = {'success': True, 'msj': 'Login Correcto'}
                else:
                    salida = {'error': True, 'msj': 'Contraseña incorrecta.'}
            else:
                salida = {'error': True, 'msj': 'Ese usuario no esta registrado, intenta nuevamente'}
        else:
            salida = {'error': True, 'msj': 'Por favor llena los todos los campos'}
    return HttpResponse(JsonResponse(salida))

def edit_user(request, id):
    user = Usuario.objects.get(id=request.user.id)
    if request.method == 'GET':
        form = UserForm(instance=user)
    else:
        form = UserForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('usuario:user_home')
    return render(request, 'usuarios/editar_perfil.html', {'form': form})


def resultados(request):
    salida = {}
    user = request.GET.get('usuario')
    if len(user) > 0:
        if request.is_ajax():
            usuarios = Usuario.objects.filter(Q(username__icontains=user)).exclude(username=request.user.username)
            results = []
            for objeto in usuarios:
                basic = {}
                basic['id'] = objeto.id
                basic['username'] = objeto.username
                results.append(basic)
            salida = {'success': True, 'objetos': results}
    return HttpResponse(JsonResponse(salida))

def follow_user(request, id):
    salida = {}
    usuario = Usuario.objects.get(id=id)
    current_user = request.user
    date = timezone.now()
    if usuario.followers.filter(id=current_user.id).exists():
        salida = {'unfollowed': True}
        usuario.followers.remove(current_user)
        current_user.following.remove(usuario)
    else:
        usuario.followers.add(current_user)
        current_user.following.add(usuario)
        texto_ = 'te ha seguido'
        ntc = Notificaciones.objects.create(
            f_user=current_user,
            fecha=date,
            s_user=usuario,
            texto=texto_
        )
        ntc.save()
        salida = {'followed': True}
    return HttpResponse(JsonResponse(salida))
