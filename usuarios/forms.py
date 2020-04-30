from django import forms
from .models import Usuario


class UserForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'username',
            'first_name',
            'last_name',
            'foto_perfil',
            'bio'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            'bio': forms.TextInput(attrs={'placeholder': 'Biografia'}),
            'foto_perfil': forms.FileInput(),
        }