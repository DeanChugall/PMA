from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import forms as auto_servis_form
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from pma_apps.users.models import Servis, Vozac

User = get_user_model()


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


class KreirajServisForm(auto_servis_form.UserCreationForm):
    role = forms.CharField(widget=forms.HiddenInput(), initial=User.Role.SERVIS)

    class Meta:
        model = Servis
        fields = ("username", "email", "role")
        error_messages = {
            "email": {
                "unique": _("Ovo EMSIL ime je vec zauzeto."),
            },
            "username": {
                "unique": _("Ovo korisnicko ime je vec zauzeto."),
            },
        }


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }
