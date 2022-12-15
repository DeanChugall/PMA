from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from pma_apps.users.models import RatingServisa, ServisProfile, VozacProfile

User = get_user_model()

admin.site.unregister(Group)

admin.site.register(ServisProfile)
admin.site.register(VozacProfile)
admin.site.register(User)
admin.site.register(RatingServisa)
