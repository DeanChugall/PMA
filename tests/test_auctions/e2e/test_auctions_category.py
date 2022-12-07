import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertURLEqual


@pytest.mark.django_db
def test_auctions_category_page_ne_autorizovani_korisnik(
    client,
    novi_jedan_vozac_autorizovan_korisnik_fixture,
    jedna_kategorija_zahteva_fixture,
):

    url_landing_page = reverse(
        "ponude:category_details_view",
        kwargs={"category_name": jedna_kategorija_zahteva_fixture.category_name},
    )
    response = client.get(url_landing_page)
    assert response.status_code == 200
    assertTemplateUsed(response, "auctions/auctions_category.html")


@pytest.mark.django_db
def test_auctions_category_page_autorizovani_korisnik(
    client,
    novi_jedan_vozac_ne_autorizovan_korisnik_fixture,
    jedna_kategorija_zahteva_fixture,
):

    url_landing_page = reverse(
        "ponude:category_details_view",
        kwargs={"category_name": jedna_kategorija_zahteva_fixture.category_name},
    )
    response = client.get(url_landing_page)
    assert response.status_code == 302
    expected_url = (
        f"/prijava?next=/ponude/kategorija/"
        f"{jedna_kategorija_zahteva_fixture.category_name}"
    ).replace(" ", "%2520")
    assertURLEqual(response.url, expected_url)
