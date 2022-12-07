from pma_apps.users.models import Vozac, VozacProfile


class TestUsersAndProfiles:
    def test_kreiraj_profil_vozaca_sa_autom(
        self, novi_jedan_vozac_sa_autom_autorizovan_korisnik_fixture
    ):

        assert VozacProfile.objects.count() == 1

        profil_vozaca = VozacProfile.objects.all().last()
        vozac = Vozac.objects.all().last()

        assert profil_vozaca.user_id == vozac.id
        assert (
            profil_vozaca.broj_telefona
            == novi_jedan_vozac_sa_autom_autorizovan_korisnik_fixture.broj_telefona
        )
        assert (
            profil_vozaca.vin
            == novi_jedan_vozac_sa_autom_autorizovan_korisnik_fixture.vin
        )
        assert (
            profil_vozaca.marka
            == novi_jedan_vozac_sa_autom_autorizovan_korisnik_fixture.marka
        )
        assert (
            profil_vozaca.modell
            == novi_jedan_vozac_sa_autom_autorizovan_korisnik_fixture.modell
        )
        assert (
            profil_vozaca.godiste
            == novi_jedan_vozac_sa_autom_autorizovan_korisnik_fixture.godiste
        )
        assert (
            profil_vozaca.kilometraza
            == novi_jedan_vozac_sa_autom_autorizovan_korisnik_fixture.kilometraza
        )
        assert (
            profil_vozaca.zapremina_motora
            == novi_jedan_vozac_sa_autom_autorizovan_korisnik_fixture.zapremina_motora
        )
        assert (
            profil_vozaca.snaga_motora
            == novi_jedan_vozac_sa_autom_autorizovan_korisnik_fixture.snaga_motora
        )
