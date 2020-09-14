# Register your models here.
from django.contrib import admin
from .models import WebAdmin, Seller, WebAdminLoginHistory, Tester, WebUser, PWGServers, PWG, PasswordHistory



# admin.site.register(User)
admin.site.register(WebAdmin)
admin.site.register(Seller)
admin.site.register(Tester)
admin.site.register(WebUser)
admin.site.register(PWGServers)
admin.site.register(PWG)
admin.site.register(WebAdminLoginHistory)
admin.site.register(PasswordHistory)
