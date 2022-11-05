from crispy_forms.bootstrap import StrictButton, InlineField, FormActions, FieldWithButtons
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Div, Layout, Row, Column
from .models import Join


class JoinForm(forms.ModelForm):
    # email = forms.EmailField(
    #     label="",
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Vaš e-mail',
    #             'aria-label': 'prijava email-a',
    #             'aria-describedby': 'button-addon1'
    #         }
    #     ))

    class Meta:
        model = Join
        fields = ['email']



    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_method = 'POST'
    #     self.helper.form_class = 'form-inline'
    #
    #     self.helper.layout = Layout(
    #         FieldWithButtons(
    #             'email',
    #             Submit('Prijava', "Prijava", css_class='btn btn-primary', attrs='hx-post="."')
    #         ),
    #     )

    # helper = FormHelper()
    # helper.add_input(Submit('submit', 'Submit', css_class='btn btn-primary'))
    # helper.form_method = 'POST'
    #
    # Div(
    #     Submit('submit', 'Log Me In', css_class='btn btn-primary'),
    #     css_class='col-lg-offset-3 col-lg-9',
    # )
