# Register your models here.
from django.contrib import admin
from .models import WebAdmin, Seller, WebAdminLoginHistory, Tester, WebUser, PWGServers, PWG, PasswordHistory, \
    TransferPwg, TransferPwgs, PwgUseRecord, SystemName, Authorize, Share, PWGHistory



# admin.site.register(User)
admin.site.register(WebAdmin)
admin.site.register(Seller)
admin.site.register(Tester)
admin.site.register(WebUser)
admin.site.register(PWGServers)
# admin.site.register(PWG)


@admin.register(PWGHistory)
class PwgAdmin(admin.ModelAdmin):
    list_display = ("pwg", "action", "object", "time", "date")


@admin.register(Authorize)
class Authorize(admin.ModelAdmin):
    list_display = ("pwg", "authorize_to", "pwgserver")


@admin.register(Share)
class Share(admin.ModelAdmin):
    list_display = ("pwg", "share_to", "pwgserver")


@admin.register(SystemName)
class SystemName(admin.ModelAdmin):
    list_display = ("serial_no", "system_name", "is_pwgs", "is_tester", "is_seller", "is_user")


@admin.register(PwgUseRecord)
class PwgUseRecord(admin.ModelAdmin):
    list_display = ("date", "time", "count", "password")


@admin.register(PWG)
class PWGAdmin(admin.ModelAdmin):
    list_display = ('name', 'owned_by', 'is_freeze', 'is_shared', 'is_authorized', 'transfer_to')


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