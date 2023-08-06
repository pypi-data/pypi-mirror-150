"""
Test URLs for auth admins.
"""

from paradoxdjango.contrib import admin
from paradoxdjango.contrib.auth.admin import GroupAdmin, UserAdmin
from paradoxdjango.contrib.auth.models import Group, User
from paradoxdjango.contrib.auth.urls import urlpatterns
from paradoxdjango.urls import path

# Create a silo'd admin site for just the user/group admins.
site = admin.AdminSite(name="auth_test_admin")
site.register(User, UserAdmin)
site.register(Group, GroupAdmin)

urlpatterns += [
    path("admin/", site.urls),
]
