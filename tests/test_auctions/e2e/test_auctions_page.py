import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_auctions_page_autorizovani_korisnik(
    client, novi_vozac_autorizovan_korisnik_fixture
):

    url_landing_page = reverse("ponude:ponude")
    response = client.get(url_landing_page)
    assert response.status_code == 200
    assertTemplateUsed(response, "auctions/auctions.html")
