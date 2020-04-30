from fotos import views
from django.urls import path
from django.contrib.auth.decorators import login_required

app_name = 'fotos'

urlpatterns = [
    path('', login_required(views.home), name="home"),
    path('postnuevo/', login_required(views.post_form), name="post_nuevo"),
    path('postear/', login_required(views.subir_foto), name="postear"),
    path('<int:id>/detalles/', login_required(views.pub_detalles), name="pub_detalles"),
    path('<int:id>/likear/', login_required(views.likear), name='likear'),
    path('<int:id>/guardar/', login_required(views.guardar_post), name='guardar'),
    path('<int:id>/comentar/', login_required(views.comentar), name='comentarios'),
    path('<int:id>/likes/', login_required(views.get_likes), name='like'),
    path('guardados/', login_required(views.get_saved), name='saved'),
    path('<int:id>/comentarios/', login_required(views.post_comments), name='comentarios_re'),
    path('buscar/', login_required(views.busqueda), name='buscar'),
    path('notificaciones/', login_required(views.notificaciones), name='ntc'),
]
