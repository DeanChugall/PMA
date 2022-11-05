from django import forms

from pma_apps.landing_page.models import Kontakti


class KontaktForma(forms.ModelForm):
    class Meta:
        model = Kontakti
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(KontaktForma, self).__init__(*args, **kwargs)
        self.fields['email'].error_messages = {
            'required': 'Polje je prazno !',
            'invalid': 'Format emaila nije ispravan !'
        }

    def clean(self):
        data = self.cleaned_data
        email = self.cleaned_data.get('email')
        if Kontakti.objects.filter(email=email):
            self.add_error("email", f"{email} vec postoji u bazi !")
        return data
