# Register your models here.
from django.contrib import admin
from .models import WebAdmin, Seller, WebAdminLoginHistory, Tester, WebUser, PWGServers, PWG, PasswordHistory, TransferPwg, TransferPwgs, PwgUseRecord



# admin.site.register(User)
admin.site.register(WebAdmin)
admin.site.register(Seller)
admin.site.register(Tester)
admin.site.register(WebUser)
admin.site.register(PWGServers)
# admin.site.register(PWG)


@admin.register(PwgUseRecord)
class PwgUseRecord(admin.ModelAdmin):
    list_display = ("date", "time", "count", "password")


@admin.register(PWG)
class PWGAdmin(admin.ModelAdmin):
    list_display = ('name', 'owned_by', 'is_freeze', 'transfer_to')


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