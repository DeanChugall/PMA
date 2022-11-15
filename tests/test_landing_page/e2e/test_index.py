import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_landing_page_autorizovani_korisnik(
    client, novi_vozac_autorizovan_korisnik_fixture
):

    url_svi_stanovi = reverse("landing_page:landing_page")
    response = client.get(url_svi_stanovi)
    assert response.status_code == 200
    assertTemplateUsed(response, "landing_page/landing_page.html")
