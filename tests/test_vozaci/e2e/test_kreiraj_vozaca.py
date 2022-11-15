import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_kreiraj_vozaca_autorizovani_korisnik(client):

    url_kreiraj_vozaca = reverse("users:kreiraj_vozaca")
    response = client.get(url_kreiraj_vozaca)
    assert response.status_code == 200
    assertTemplateUsed(response, "vozaci/kreiraj_vozaca.html")
