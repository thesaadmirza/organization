from django.contrib import admin
from organizations.models import (Organization, OrganizationUser,
                                  OrganizationOwner)
from accounts.forms import AccountUserForm
from accounts.models import Account, AccountUser


class AccountUserAdmin(admin.ModelAdmin):
    form = AccountUserForm


admin.site.register(Account)
admin.site.register(AccountUser, AccountUserAdmin)
