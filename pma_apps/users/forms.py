from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _

from pma_apps.users.models import Vozac

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
        "invalid_login": _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }


class KreirajVozacaForm(admin_forms.UserCreationForm):
    role = forms.CharField(widget=forms.HiddenInput(), initial=User.Role.SERVIS)
    username = forms.CharField(help_text=None, label="Korisničko Ime: ")
    password1 = forms.CharField(
        help_text=None,
    )
    password2 = forms.CharField(
        help_text=None,
    )

    class Meta:
        model = Vozac
        fields = (
            "username",
            "role",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class DetaljiVozacaForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Vozac
        fields = (
            "role",
            "name",
            "last_name",
            "email",
            "username",
        )


class UrediVozaciForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Vozac
        fields = ["first_name", "last_name", "email"]


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "name",
        )
        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }
