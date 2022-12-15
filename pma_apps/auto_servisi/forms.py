from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from pma_apps.users.models import Servis

User = get_user_model()


class DetaljiServisKorisnikaForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Servis
        fields = [
            "role",
            "last_name",
            "email",
            "username",
        ]


class KreirajServisKorisnikaForm(UserCreationForm):
    # role = forms.CharField(widget=forms.HiddenInput(), initial=User.Role.VOZAC)
    first_name = forms.CharField(required=True, help_text="Ime*", label="")
    last_name = forms.CharField(required=True, help_text="Prezime*", label="")
    email = forms.EmailField(
        required=True, help_text="E-Mail*", label="", widget=forms.EmailInput()
    )
    username = forms.CharField(required=True, help_text="Korisničko Ime*", label="")
    password1 = forms.CharField(required=True, help_text="Lozinka*", label="")
    password2 = forms.CharField(required=True, help_text="Potvrdi lozinku*", label="")

    class Meta:
        model = Servis
        fields = [
            "first_name",
            "last_name",
            "grad",
            "username",
            "email",
            "password1",
            "password2",
        ]
