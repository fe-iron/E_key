from modeltranslation.translator import register, TranslationOptions
from .models import WebAdmin, WebUser, Seller, Tester, WebAdminLoginHistory, PasswordHistory


@register(WebAdmin)
class WebAdminTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name', 'email', 'alias', 'phone', 'system_name',)


@register(WebUser)
class WebUserTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name', 'email', 'alias', 'phone', 'system_name',)


@register(Seller)
class SellerTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name', 'email', 'alias', 'phone', 'system_name',)


@register(Tester)
class TesterTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name', 'email', 'alias', 'phone', 'system_name',)


@register(WebAdminLoginHistory)
class WebAdminLoginHistoryTranslationOptions(TranslationOptions):
    fields = ('device_name',)


@register(PasswordHistory)
class PasswordHistoryTranslationOptions(TranslationOptions):
    fields = ('login_time', 'login_date', 'device_name', 'last_pass')
