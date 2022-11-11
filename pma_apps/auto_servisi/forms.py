from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from pma_apps.users.models import Servis

User = get_user_model()


class DetaljiVozacaForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Servis
        fields = (
            "role",
            "name",
            "last_name",
            "email",
            "username",
        )


class KreirajServisForm(UserCreationForm):
    role = forms.CharField(widget=forms.HiddenInput(), initial=User.Role.SERVIS)
    username = forms.CharField(help_text=None, label="Korisničko Ime: ")
    password1 = forms.CharField(
        help_text=None,
    )
    password2 = forms.CharField(
        help_text=None,
    )

    class Meta:
        model = Servis
        fields = (
            "username",
            "role",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
        help_texts = {
            "username": None,
            "email": None,
        }
        help_text = {
            "password1": None,
            "password2": None,
        }
