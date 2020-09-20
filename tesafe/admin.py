# Register your models here.
from django.contrib import admin
from .models import WebAdmin, Seller, WebAdminLoginHistory, Tester, WebUser, PWGServers, PWG, PasswordHistory, TransferPwg, TransferPwgs



# admin.site.register(User)
admin.site.register(WebAdmin)
admin.site.register(Seller)
admin.site.register(Tester)
admin.site.register(WebUser)
admin.site.register(PWGServers)
# admin.site.register(PWG)


@admin.register(PWG)
class PWGAdmin(admin.ModelAdmin):
    list_display = ('name', 'owned_by', 'transfer_to')


admin.site.register(WebAdminLoginHistory)
admin.site.register(PasswordHistory)
# admin.site.register(TransferPwg)
@admin.register(TransferPwg)
class TransferPwgAdmin(admin.ModelAdmin):
    list_display = ('pwg_owner', 'pwgs_owner', 'user')


# admin.site.register(TransferPwgs)

@admin.register(TransferPwgs)
class TransferPwgsAdmin(admin.ModelAdmin):
    list_display = ('pwgs_owner', 'user')