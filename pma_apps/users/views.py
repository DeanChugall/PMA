from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

User = get_user_model()


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
