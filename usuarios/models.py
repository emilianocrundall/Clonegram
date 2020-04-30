from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Usuario(AbstractUser):
    foto_perfil = models.ImageField(blank=True, null=True, upload_to='covers/%Y/%m/%D/')
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, symmetrical=False, related_name='userfollowers')
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, symmetrical=False, related_name='userfollowing')
    bio = models.CharField(max_length=400, blank=True)

    @property
    def count_followers(self):
        return self.followers.count()
    
    @property
    def count_following(self):
        return self.following.count()
