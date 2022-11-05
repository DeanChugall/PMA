from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from pma_apps.landing_page.forms import KontaktForma


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
        print(f"CONTEXT: {context}")
    return render(request, "landing_page/partials/kontakt_hello_message.html", context=context)
