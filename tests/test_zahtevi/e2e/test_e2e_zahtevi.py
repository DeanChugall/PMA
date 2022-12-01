import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_kreiraj_vozaca_autorizovani_korisnik(
    client, novi_jedan_vozac_autorizovan_korisnik_fixture
):
    url_kreiraj_vozaca = reverse("ponude:kreiranje_zahteva")
    response = client.get(url_kreiraj_vozaca)
    assert response.status_code == 200
    assertTemplateUsed(response, "auctions/kreiranje_zahteva.html")


@pytest.mark.django_db
def test_kreiraj_vozaca_ne_autorizovani_korisnik(
    client, novi_jedan_vozac_ne_autorizovan_korisnik_fixture
):
    url_kreiraj_vozaca = reverse("ponude:kreiranje_zahteva")
    response = client.get(url_kreiraj_vozaca)
    assert response.status_code == 302
