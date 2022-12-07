import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertURLEqual


@pytest.mark.django_db
def test_edit_detalji_vozaca_url_autorizovani_korisnik(
    client, novi_jedan_vozac_autorizovan_korisnik_fixture
):
    url_kreiraj_vozaca = reverse(
        "users:detalji_vozaca",
        args=[novi_jedan_vozac_autorizovan_korisnik_fixture.username],
    )
    response = client.get(url_kreiraj_vozaca)
    assert response.status_code == 200
    assertTemplateUsed(response, "vozaci/detalji-vozaca.html")


@pytest.mark.django_db
def test_edit_detalji_vozaca_url_ne_autorizovani_korisnik(
    client, novi_jedan_vozac_ne_autorizovan_korisnik_fixture
):
    url_kreiraj_vozaca = reverse(
        "users:detalji_vozaca",
        args=[novi_jedan_vozac_ne_autorizovan_korisnik_fixture.username],
    )
    response = client.get(url_kreiraj_vozaca)
    assert response.status_code == 302
    expected_url = (
        f"/prijava?next=/detalji-vozaca/"
        f"{novi_jedan_vozac_ne_autorizovan_korisnik_fixture.username}/"
    )
    assertURLEqual(response.url, expected_url)
