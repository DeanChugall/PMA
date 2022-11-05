from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import FormView
from django.views import generic
from django.urls import reverse
from pma_apps.contacts.forms import JoinForm
from pma_apps.contacts.models import Join


class LandingPageView(SuccessMessageMixin, generic.CreateView):
    template_name = 'landing_page/landing_page.html'
    form_class = JoinForm
    success_message = "%(email)s was created successfully"
    context_object_name = 'joined'

    def get_success_url(self):
        return reverse('landing_page:landing_page')
        # return reverse('landing_page:landing_page')

    # def get(self, request, *args, **kwargs):
    #     return render(request, "landing_page/landing_page.html")


def join_hello_message(request):
    email = request.POST.get("email")
    email = Join.objects.create(email=email)
    # return HttpResponse(f"Hava sto ste se prijavili: {email} !!!")
    return render(request, "landing_page/partials/join-form.html", {'email':email})
