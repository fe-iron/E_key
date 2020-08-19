# Register your models here.
from django.contrib import admin
from .models import WebAdmin, Seller, WebAdminLoginHistory, Tester, WebUser



# admin.site.register(User)
admin.site.register(WebAdmin)
admin.site.register(Seller)
admin.site.register(Tester)
admin.site.register(WebUser)
admin.site.register(WebAdminLoginHistory)
