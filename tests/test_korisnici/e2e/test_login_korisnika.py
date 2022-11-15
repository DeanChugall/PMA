import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_login_korisnika(client):

    url_login_korisnika = reverse("users:prijava")
    response = client.get(url_login_korisnika)
    assert response.status_code == 200
    assertTemplateUsed(response, "account/login.html")
