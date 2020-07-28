from django.conf.urls import url
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
    path("register-next", views.register_next, name="register-next"),
    path("seller-home", views.seller_home, name="seller-home"),
    path("seller-user", views.seller_user, name="seller-user"),
    path("seller-pwg", views.seller_pwg, name="seller-pwg"),
    path("names_view", views.names_view, name="names-view"),
    path("transfer", views.transfer, name="transfer"),
    path("tester-getback", views.tester_getback, name="tester-getback"),
    path("tester-tested-pwg-list", views.tester_tested_pwg_list, name="tester-tested-pwg-list"),
    path("pwg-sublist", views.pwg_sublist, name="pwg-sublist"),
    path("pwg-getback", views.pwg_getback, name="pwg-getback"),
    path("pwg-getback-sublist", views.pwg_getback_sublist, name="pwg-getback-sublist"),
    path("tester-pwg-sublist", views.tester_pwg_sublist, name="pwg-getback-sublist"),
    path("transfer-seller", views.transfer_seller, name="transfer-seller"),
    path("seller-authorized", views.seller_authorized, name="seller-authorized"),
    path("seller-deauthorized", views.seller_deauthorized, name="seller-deauthorized"),
    path("seller-shared", views.seller_shared, name="seller-shared"),
    path("seller-deshared", views.seller_deshared, name="seller-deshared"),
    path("seller-pwg-transfer", views.seller_pwg_transfer, name="seller-pwg-transfer"),

    # path("webAdmin_register", views.webAdmin_register.as_view(), name="webAdmin_register"),

]
