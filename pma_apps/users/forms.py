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


class UlogujVozacaForm(AuthenticationForm):
    username = UsernameField(
        label=_(""),
        strip=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Korisničko Ime",
                "class": "input100 border-start-0 form-control ms-0",
            }
        ),
    )
    password = forms.CharField(
        label=_(""),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Lozinka",
                "type": "password",
            }
        ),
    )

    error_messages = {
        "invalid_login": _("Došlo je do greške,proverite Vaše pristupne podatke."),
        "inactive": _("This account is inactive."),
    }


class KreirajVozacaForm(UserCreationForm):
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
        model = Vozac
        fields = [
            "first_name",
            "last_name",
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
    broj_telefona = forms.CharField(
        required=False, help_text="broj_telefona*", label=""
    )
    vin = forms.CharField(required=False, help_text="vin*", label="")
    marka = forms.CharField(required=False, help_text="marka", label="")
    first_name = forms.CharField(required=False, help_text="first_name", label="")

    class Meta:
        model = VozacProfile
        fields = [
            "broj_telefona",
        ]


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
        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }
