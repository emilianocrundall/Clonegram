from usuarios import views
from django.urls import path
from django.contrib.auth.decorators import login_required

app_name = 'usuario'

urlpatterns = [
    path('loginhome/', views.login_home, name='login_home'),
    path('registrarsehome/', views.registrarse_home, name='registrarse_home'),
    path('registrarse/', views.registrarse, name='registrarse'),
    path('login/', views.login_user, name='login'),
    path('home/', login_required(views.user_home), name='user_home'),
    path('<int:id>/editar/', login_required(views.edit_user), name='editar'),
    path('<int:id>/perfil/', login_required(views.user_profile), name='user_profile'),
    path('resultados/', login_required(views.resultados), name='resultados'),
    path('<int:id>/follow/', login_required(views.follow_user), name='follow'),
]
