from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
    UsernameField,
)
from django.utils.translation import gettext_lazy as _

from pma_apps.users.models import Vozac, VozacProfile

User = get_user_model()


class UserAdminChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            "username",
        ]
        error_messages = {"username": {"unique": _("Ovo korisničko Ime je zauzeto.")}}


class UlogujVozacaForm(AuthenticationForm):
    username = UsernameField(
        label=_(""),
        strip=True,
    )
    password = forms.CharField(
        label=_(""),
        strip=True,
        widget=forms.PasswordInput(
            attrs={
                "required": "required",
            }
        ),
    )

    error_messages = {
        "invalid_login": _("Došlo je do greške,proverite Vaše pristupne podatke."),
        "inactive": _("Vaš Nalog Nije Aktivan."),
    }


class KreirajVozacaForm(UserCreationForm):
    first_name = forms.CharField(required=True, help_text="Ime*", label="")
    last_name = forms.CharField(required=True, help_text="Prezime*", label="")
    email = forms.EmailField(
        required=True, help_text="E-Mail*", label="", widget=forms.EmailInput()
    )
    username = forms.CharField(required=True, help_text="Korisničko Ime*", label="")
    password1 = forms.CharField(required=True, help_text="Lozinka*", label="")
    password2 = forms.CharField(required=True, help_text="Potvrdi lozinku*", label="")

    class Meta:
        model = Vozac
        fields = [
            "first_name",
            "last_name",
            "grad",
            "username",
            "email",
            "password1",
            "password2",
        ]


class DetaljiVozacaForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Vozac
        fields = [
            "role",
            "last_name",
            "first_name",
            "email",
            "username",
        ]


class UrediVozacaForm(forms.ModelForm):
    class Meta:
        model = Vozac
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


class UrediProfilVozacaForm(forms.ModelForm):
    class Meta:
        model = VozacProfile
        fields = [
            "broj_telefona",
            "vin",
            "marka",
            "modell",
            "vrsta_goriva",
            "kilometraza",
            "godiste",
            "snaga_motora",
            "zapremina_motora",
        ]
