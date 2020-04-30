from django.db import models
from django.conf import settings

class Post(models.Model):
    imagen = models.ImageField(blank=True, null=True, upload_to='covers/%Y/%m/%D/')
    fecha = models.DateField(auto_now_add=True)
    pie = models.CharField(max_length=500)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    guardar = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='guardar')

    def __str__(self):
        return self.pie

    @property
    def num_likes(self):
        padre = self.likes.count()
        return padre
    
    @property
    def comments(self):
        return self.comentarios.all()


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_likes'
    )
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user

class ComentarioPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.CharField(max_length=200)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.texto

class Notificaciones(models.Model):
    f_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='current_user',
        blank=True, null=True
    )
    texto = models.CharField(max_length=50)
    s_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    fecha = models.DateField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
