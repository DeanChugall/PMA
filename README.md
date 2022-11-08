# PMA project

---

[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Python](https://img.shields.io/badge/HTML%20code%20style-djhtml-orange?logo=html5)](https://github.com/rtts/djhtml)
[![Python](https://img.shields.io/badge/python-3.11.0-blue.svg?logo=python&logoColor=yellow)](https://www.python.org/)

## Integracija sa Digital Ocean APP platformom

- Napravljen **STAGE server** na APP Digital Ocean platformi [Link ka APP-u](https://pma-app-k89y6.ondigitalocean.app/).
- U
  sekciji [APP / SETTINGS / DOMAIN](https://cloud.digitalocean.com/apps/8058ee2c-a1c4-420f-bb1c-534672111037/settings?i=8d2545)
  dodati domain name: **popravimojauto.com**.
- Zatim na CloudFlare dodati ponudjenu CNAME varijablu !

---

## Korisne komande:
- Ciscenje svi paketa iz PIP-a: ```pip freeze | xargs pip uninstall -y```
- Pre-Commit run: ```pre-commit run```
- HTML pre-commit: ```djhtml -i pma_apps/templates/.```
