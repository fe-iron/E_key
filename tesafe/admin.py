# Register your models here.
from django.contrib import admin
from .models import WebAdmin, Seller, WebAdminLoginHistory, Tester, WebUser, PWGServers, PWG, PasswordHistory, \
    TransferPwg, TransferPwgs, PwgUseRecord, SystemName, Authorize, Share, PWGHistory, TesterPWGHistory, UserToUser, \
    MessageModel, UserLogin, Notification, TestedPWGHistory


# admin.site.register(User)
admin.site.register(WebAdmin)
admin.site.register(Seller)
admin.site.register(Tester)
admin.site.register(WebUser)
admin.site.register(PWGServers)
admin.site.register(TesterPWGHistory)
# admin.site.register(PWG)


@admin.register(PWGHistory)
class PwgAdmin(admin.ModelAdmin):
    list_display = ("pwg", "action", "object", "time", "date")


@admin.register(TestedPWGHistory)
class TestedPWGHistoryAdmin(admin.ModelAdmin):
    list_display = ("pwg_name", "tester", "date", "time")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'type')


@admin.register(Authorize)
class Authorize(admin.ModelAdmin):
    list_display = ("pwg", "authorize_to", "pwgserver")


@admin.register(UserLogin)
class UserLogin(admin.ModelAdmin):
    list_display = ("user", "session_key", "acctype", "timestamp")


@admin.register(Share)
class Share(admin.ModelAdmin):
    list_display = ("pwg", "share_to", "pwgserver")


@admin.register(SystemName)
class SystemName(admin.ModelAdmin):
    list_display = ("serial_no", "system_name", "is_pwgs", "is_tester", "is_seller", "is_user")


@admin.register(PwgUseRecord)
class PwgUseRecord(admin.ModelAdmin):
    list_display = ("date", "time", "password", "pwg")


@admin.register(PWG)
class PWGAdmin(admin.ModelAdmin):
    list_display = ('name', 'owned_by', 'is_freeze', 'is_shared', 'is_authorized', 'transfer_to')


admin.site.register(WebAdminLoginHistory)
admin.site.register(PasswordHistory)


@admin.register(TransferPwg)
class TransferPwgAdmin(admin.ModelAdmin):
    list_display = ('pwg_owner', 'pwgs_owner', 'user')


# admin.site.register(TransferPwgs)

@admin.register(TransferPwgs)
class TransferPwgsAdmin(admin.ModelAdmin):
    list_display = ('pwgs_owner', 'user')


@admin.register(UserToUser)
class UserToUserAdmin(admin.ModelAdmin):
    list_display = ("date_time", "main_user", "associated_user")


class MessageModelAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)
    search_fields = ('id', 'body', 'user__username', 'recipient__username')
    list_display = ('id', 'user', 'recipient', 'timestamp', 'body')
    list_display_links = ('id',)
    list_filter = ('user', 'recipient')
    date_hierarchy = 'timestamp'


admin.site.register(MessageModel, MessageModelAdmin)
