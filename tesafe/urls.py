from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("admin-home", views.admin_home, name="admin-home"),
    path("admin-seller", views.admin_seller, name="admin-seller"),
    path("admin-tester", views.admin_tester, name="admin-tester"),
    path("admin-seller", views.admin_seller, name="admin-seller"),
    path("admin-info-server", views.admin_info_server, name="admin-info-server"),
    path("register_next", views.register_next, name="register_next"),
    # path("webAdmin_register", views.webAdmin_register.as_view(), name="webAdmin_register"),

]
