from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from pma_apps.landing_page.forms import KontaktForma, EmailForma


class LandingPageView(SuccessMessageMixin, generic.CreateView):
    template_name = 'landing_page/landing_page.html'
    form_class = KontaktForma
    success_message = "%(email)s was created successfully"
    context_object_name = 'kontakti'

    def get_success_url(self):
        return reverse('landing_page:landing_page')


def kontakt_hello_message(request):
    form = KontaktForma(request.POST or None)
    context = {
        'form': form,
    }

    if form.is_valid():
        kontakti_obj = form.save()
        context['form'] = KontaktForma()
        context['object'] = kontakti_obj
        context['kreiran'] = True
    return render(request, "landing_page/partials/kontakt_hello_message.html", context=context)


def send_email(request):
    if request.method == "GET":
        form = EmailForma()
    else:
        form = EmailForma(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            ime = cleaned_data["ime"]
            tema = cleaned_data["tema"]
            email = cleaned_data["email"]
            pitanje = cleaned_data['pitanje']
            if not ime or tema or email or pitanje:
                try:
                    send_mail(tema, f'\nPitanje: {pitanje}\nIme:{ime}\nEmail: {email}', email,
                              ["info@popravimojauto.com"])
                except BadHeaderError:
                    return HttpResponse("Invalid header found.")
                return render(request, "landing_page/partials/send_email.html", {"form": form})
    return render(request, "landing_page/partials/send_email.html", {"form": form})
