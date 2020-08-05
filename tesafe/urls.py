from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    # admin urls
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("admin-home", views.admin_home, name="admin-home"),
    path("admin-seller", views.admin_seller, name="admin-seller"),
    path("admin-tester", views.admin_tester, name="admin-tester"),
    path("admin-info-server", views.admin_info_server, name="admin-info-server"),
    path("transfer", views.transfer, name="transfer"),
    path("tester-getback", views.tester_getback, name="tester-getback"),
    path("tester-tested-pwg-list", views.tester_tested_pwg_list, name="tester-tested-pwg-list"),
    path("pwg-sublist", views.pwg_sublist, name="pwg-sublist"),
    path("pwg-getback", views.pwg_getback, name="pwg-getback"),
    path("pwg-getback-sublist", views.pwg_getback_sublist, name="pwg-getback-sublist"),
    path("tester-pwg-sublist", views.tester_pwg_sublist, name="pwg-getback-sublist"),

    # seller PWG
    path("seller-home", views.seller_home, name="seller-home"),
    path("seller-user", views.seller_user, name="seller-user"),
    path("seller-pwg", views.seller_pwg, name="seller-pwg"),
    path("transfer-seller", views.transfer_seller, name="transfer-seller"),
    path("transfer-seller-pwg", views.transfer_seller_pwg, name="transfer-seller-pwg"),
    path("seller-authorized", views.seller_authorized, name="seller-authorized"),
    path("seller-authorized-pwg", views.seller_authorized_pwg, name="seller-authorized-pwg"),
    path("seller-deauthorized-pwg", views.seller_deauthorized_pwg, name="seller-deauthorized-pwg"),
    path("seller-shared", views.seller_shared, name="seller-shared"),
    path("seller-shared-pwg", views.seller_shared_pwg, name="seller-shared-pwg"),
    path("seller-deshared-pwg", views.seller_deshared_pwg, name="seller-deshared-pwg"),
    path("seller-pwg-transfer", views.seller_pwg_transfer, name="seller-pwg-transfer"),

    # path("webAdmin_register", views.webAdmin_register.as_view(), name="webAdmin_register"),

]
