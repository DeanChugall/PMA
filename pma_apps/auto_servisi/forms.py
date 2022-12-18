from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from pma_apps.users.models import Servis, ServisProfile

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


class UrediServisForm(forms.ModelForm):
    class Meta:
        model = Servis
        fields = [
            "role",
            "last_name",
            "grad",
            "first_name",
            "email",
            "username",
        ]
        widgets = {
            "role": forms.TextInput(attrs={"type": "hidden"}),
        }


class UrediProfilServisaForm(forms.ModelForm):
    class Meta:
        model = ServisProfile
        fields = [
            "radni_dan",
            "otvoreno_do",
            "otvoreno_od",
            "slika_logo_servisa",
            "broj_telefona_servisa",
            "slika_servisa",
            "ime_servisa",
            "opis_servisa",
            "adresa_servisa",
            "datum_osnivanja",
            "facebook_link",
            "youtube_link",
            "twitter_link",
            "linkedin_link",
            "header",
        ]
