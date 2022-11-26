from django.urls import reverse


def test_root_url_for_detalji_ponude(client, db):
    """Test lista stanova API end point"""
    url = reverse("ponude:ponude")
    response = client.get(url, format="json")
    print("RESPONSE(test_lista_stanova_API_end_point): " + str(response))
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_detalji_vozaca_autorizovani_korisnik(
#     client, novi_vozac_autorizovan_korisnik_fixture
# ):
#
#     url_landing_page = reverse(
#         "ponude:detalji_ponude_view", kwargs={'zahtev_id': 1}
#     )
#     response = client.get(url_landing_page)
#     assert response.status_code == 200
#     assertTemplateUsed(response, "auctions/detalji_ponude.html")
