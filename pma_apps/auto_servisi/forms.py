from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from pma_apps.users.models import Servis, ServisProfile, SlikaLogoServisa, SlikeServisa

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
            "otvoreno_od_ponedeljak_petak",
            "otvoreno_do_ponedeljak_petak",
            "otvoreno_od_subota",
            "otvoreno_do_subota",
            "otvoreno_od_nedelja",
            "otvoreno_do_nedelja",
            "slika_logo_servisa",
            "specijalizovan_za_marku",
            "slika_servisa",
            "broj_telefona_servisa",
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


class ImageServisaForm(forms.ModelForm):
    """
    A ModelForm class for adding an image to the auction
    """

    class Meta:
        model = SlikeServisa
        fields = ["slika_servisa"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slika_servisa"].label = ""
        self.visible_fields()[0].field.widget.attrs["class"] = "form-control"


class ImageLogoaServisaForm(forms.ModelForm):
    """
    A ModelForm class for adding an image to the auction
    """

    class Meta:
        model = SlikaLogoServisa
        fields = ["slika_logo_servisa"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slika_logo_servisa"].label = ""
        self.visible_fields()[0].field.widget.attrs["class"] = "form-control"
