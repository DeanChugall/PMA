from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from pma_apps.users.models import Vozac

User = get_user_model()


class KreirajVozacaForm(admin_forms.UserCreationForm):
    role = forms.CharField(widget=forms.HiddenInput(), initial=User.Role.SERVIS)
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


class UpdateVozaciForm(forms.ModelForm):
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
