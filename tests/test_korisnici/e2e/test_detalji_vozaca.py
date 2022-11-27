import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_detalji_vozaca_autorizovani_korisnik(
    client, novi_jedan_vozac_autorizovan_korisnik_fixture
):

    url_landing_page = reverse(
        "users:detalji_vozaca",
        args=[novi_jedan_vozac_autorizovan_korisnik_fixture.username],
    )
    response = client.get(url_landing_page)
    assert response.status_code == 200
    assertTemplateUsed(response, "vozaci/detalji-vozaca.html")
