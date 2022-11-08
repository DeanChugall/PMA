from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from pma_apps.users.forms import DetaljiVozacaForm
from pma_apps.users.models import Vozac

User = get_user_model()


class DetaljiVozacaView(LoginRequiredMixin, generic.DetailView):
    template_name = 'users/user_detail.html'
    queryset = Vozac.objects.all()
    context_oject_name = "detalji_vozaca"


class UrediKupcaView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'users/user_detail.html'
    queryset = Vozac.objects.all()
    form_class = DetaljiVozacaForm
    context_object_name = "uredi_vozaca"

    def get_success_url(self):
        return reverse('landing_page:landing_page')


def login(request):
    return HttpResponseRedirect(settings.LOGIN_URL)


@login_required
def logout(request):
    django_logout(request)
    redirect_uri = request.build_absolute_uri("/")
    url = "https://{}/v2/logout?".format(settings.SOCIAL_AUTH_AUTH0_DOMAIN) + urlencode(
        {
            "client_id": settings.SOCIAL_AUTH_AUTH0_KEY,
            "returnTo": redirect_uri,
        }
    )

    return HttpResponseRedirect(url)

# def profile(request, username):
#     if request.method == "POST":
#         user = request.user
#         form = UserUpdateForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             user_form = form.save()
#             messages.success(request, f'{user_form.username}, Your profile has been updated!')
#             print(request, f'{user_form.username}, Your profile has been updated!')
#             return redirect("users:profile", user_form.username)
#
#         for error in list(form.errors.values()):
#             messages.error(request, error)
#
#     user = get_user_model().objects.filter(username=username).first()
#     if user:
#         form = UserUpdateForm(instance=user)
#         return render(
#             request=request,
#             template_name="users/profile.html",
#             context={"form": form}
#         )
#
#     return redirect("landing_page:landing_page")

# def profile(request, username):
#     if request.method == "POST":
#         user = request.user
#         form = UserUpdateForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             user_form = form.save()
#             messages.success(request, f'{user_form.username}, Your profile has been updated!')
#             print(request, f'{user_form.username}, Your profile has been updated!')
#             return redirect("users:profile", user_form.username)
#
#         for error in list(form.errors.values()):
#             messages.error(request, error)
#
#     user = get_user_model().objects.filter(username=username).first()
#     if user:
#         form = UserUpdateForm(instance=user)
#         return render(
#             request=request,
#             template_name="users/profile.html",
#             context={"form": form}
#         )
#
#     return redirect("landing_page:landing_page")
