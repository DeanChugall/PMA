from pma_apps.users.models import *  # noqa


class TestUsersAndProfiles:
    def test_broj_profila_servisa(self, novi_jedan_servis_ne_autorizovan_fixture):
        Servis.objects.create(  # noqa
            username="servis2",
            password="servis2",
            email="servis2@servis2.com",
            first_name="servis2",
            last_name="servis2",
        )
        svi_servisi_from_db = Servis.objects.all()  # noqa
        profil_servisa_from_db = ServisProfile.objects.all()  # noqa
        assert Vozac.objects.count() == svi_servisi_from_db.count()  # noqa
        print(
            f"BROJ svi_servisi_from_db<<<<<<<<<< {svi_servisi_from_db.count()}"
        )  # noqa
        print(f"BROJ PROFILAAAAAA<<<<<<<<<< {profil_servisa_from_db.count()}")  # noqa

    def test_broj_profila_vozaca(
        self, novi_jedan_vozac_ne_autorizovan_korisnik_fixture
    ):
        Vozac.objects.create(  # noqa
            username="dejan_no_auth_vozac1",
            password="dejan_no_auth_vozac1",
            role="VOZAC",
            email="dejan_no_auth_vozac1@dejan_no_auth_vozac.com",
            first_name="dejan_no_auth_vozac1",
            last_name="dejan_no_auth_vozac1",
        )
        svi_vozaci_from_db = Vozac.objects.all()  # noqa
        profil_vozaca_from_db = VozacProfile.objects.all()  # noqa
        assert Vozac.objects.count() == svi_vozaci_from_db.count()  # noqa
        print(f"BROJ svi_vozaci_from_db<<<<<<<<<< {svi_vozaci_from_db.count()}")
        print(f"BROJ PROFILAAAAAA<<<<<<<<<< {profil_vozaca_from_db.count()}")
        # # Provera poklapanja broja profila Vozaca i korisnika Vozaca
        # broj_korisnika_vozaca = svi_vozaci_from_db.count()
        # broj_profila_vozaca = profil_vozaca_from_db.count()
        # assert broj_korisnika_vozaca == broj_profila_vozaca
        #
        # pogresan_broj_korisnika_vozaca = random.randint(1000, 10000)
        # assert pogresan_broj_korisnika_vozaca != broj_profila_vozaca

    # def test_kreiranje_jednog_no_auth_vozaca(self, novi_jedan_vozac_ne_autorizovan_korisnik_fixture):
    #     vozac_from_db = Vozac.objects.all()
    #     email = vozac_from_db[0].email
    #     pogresan_email = "pogresan-mail@pogresan-mail.com"
    #     username = vozac_from_db[0].username
    #     pogresan_username = "pogresan-username"
    #
    #     assert Vozac.objects.count() == 1
    #     assert novi_jedan_vozac_ne_autorizovan_korisnik_fixture.email == email
    #     assert novi_jedan_vozac_ne_autorizovan_korisnik_fixture.email != pogresan_email
    #     assert novi_jedan_vozac_ne_autorizovan_korisnik_fixture.username == username
    #     assert novi_jedan_vozac_ne_autorizovan_korisnik_fixture.username != pogresan_username

    # def test_kreiranje_jednog_auth_vozaca(self, novi_jedan_vozac_autorizovan_korisnik_fixture):
    #     assert Vozac.objects.count() == 1
    #
    # def test_kreiranje_dva_vozaca(
    #     self,
    #     novi_jedan_vozac_autorizovan_korisnik_fixture,
    #     novi_jedan_vozac_ne_autorizovan_korisnik_fixture):
    #     assert Vozac.objects.count() == 2
    #
    #
    # def test_provera_id_u_profilu_i_vozacu(self, novi_jedan_vozac_ne_autorizovan_korisnik_fixture):
    #     # Provera id Vozaca i id u Profilu Vozaca
    #     id_user_vozaca_from_db = novi_jedan_vozac_ne_autorizovan_korisnik_fixture.id
    #
    #     # Get objekat profila Vozaca
    #     profil_vozaca = VozacProfile.objects.get(
    #         user_id=id_user_vozaca_from_db
    #     )
    #
    #     assert id_user_vozaca_from_db == profil_vozaca.user_id
    #
    #     pogresan_id_profil_vozaca = "1234"
    #     assert id_user_vozaca_from_db != pogresan_id_profil_vozaca
    #
    # def test_provera_polja_profila_vozaca(self, novi_jedan_vozac_ne_autorizovan_korisnik_fixture):
    #
    #     id_user_vozaca_from_db = novi_jedan_vozac_ne_autorizovan_korisnik_fixture.id
    #     profil_vozaca = VozacProfile.objects.get(
    #         user_id=id_user_vozaca_from_db
    #     )
    #
    #     # Provera polja profila Vozaca
    #     profil_vozaca.broj_telefona = "+381 63 111 222 333"
    #     profil_vozaca.save()
    #     broj_telefona_iz_profila = VozacProfile.objects.get(broj_telefona="+381 63 111 222 333")
    #     assert broj_telefona_iz_profila.broj_telefona == profil_vozaca.broj_telefona
    #
    #     pogresan_broj_telefona_profila = random.randint(1000, 10000)
    #     assert pogresan_broj_telefona_profila != broj_telefona_iz_profila.broj_telefona
