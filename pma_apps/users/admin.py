from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from pma_apps.users.models import Servis, Vozac

User = get_user_model()

admin.site.unregister(Group)

admin.site.register(Vozac)
admin.site.register(Servis)
admin.site.register(User)


# @admin.register(User)
# class UserAdmin(auth_admin.UserAdmin):
#
#     form = UserAdminChangeForm
#     add_form = UserAdminCreationForm
#     fieldsets = (
#         (None, {"fields": ("username", "password")}),
#         (_("Personal info"), {"fields": ("email")}),
#         (
#             _("Permissions"),
#             {
#                 "fields": (
#                     "is_active",
#                     "is_staff",
#                     "is_superuser",
#                     # "groups",
#                     # "user_permissions",
#                 ),
#             },
#         ),
#         (_("Important dates"), {"fields": ("last_login", "date_joined")}),
#     )
#     list_display = ["username" , "is_superuser"]
#     search_fields = ["username"]
