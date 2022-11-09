from django import forms

from pma_apps.landing_page.models import Kontakti


class KontaktForma(forms.ModelForm):
    class Meta:
        model = Kontakti
        fields = [
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].error_messages = {
            "required": "Polje je prazno !",
            "invalid": "Format emaila nije ispravan !",
        }

    def clean(self):
        data = self.cleaned_data
        email = self.cleaned_data.get("email")
        if Kontakti.objects.filter(email=email):
            self.add_error("email", f"{email} vec postoji u bazi !")
        return data


class EmailForma(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].error_messages = {
            "required": 'Polje "Email" je prazno !',
            "invalid": "Format emaila nije ispravan !",
        }
        self.fields["ime"].error_messages = {
            "required": 'Polje "Ime" je prazno !',
            "invalid": "Format unosa imena nije ispravan !",
        }
        self.fields["tema"].error_messages = {
            "required": 'Polje "Tema" je prazno !',
            "invalid": "Format unosa teme nije ispravan !",
        }
        self.fields["pitanje"].error_messages = {
            "required": 'Polje "Pitanje" je prazno !',
            "invalid": "Format unosa pitanja nije ispravan !",
        }

    ime = forms.CharField()
    email = forms.EmailField()
    tema = forms.CharField()
    pitanje = forms.CharField()
