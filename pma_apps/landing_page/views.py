from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic import FormView
from django.views import generic
from django.urls import reverse
from pma_apps.contacts.forms import JoinForm


class LandingPageView(SuccessMessageMixin, generic.CreateView):
    template_name = 'landing_page/landing_page.html'
    form_class = JoinForm
    success_message = "%(email)s was created successfully"
    def get_success_url(self):
        return reverse('landing_page:landing_page')
        # return reverse('landing_page:landing_page')


    # def get(self, request, *args, **kwargs):
    #     return render(request, "landing_page/landing_page.html")
