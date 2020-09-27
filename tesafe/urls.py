from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    # admin urls
    path("", views.index, name="index"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("admin-home", views.admin_home, name="admin-home"),
    path("admin-seller", views.admin_seller, name="admin-seller"),
    path("admin-tester", views.admin_tester, name="admin-tester"),
    path("admin-info-server", views.admin_info_server, name="admin-info-server"),
    path("transfer<int:id>", views.transfer, name="transfer"),
    path("tester-getback<int:id>", views.tester_getback, name="tester-getback"),
    path("tester-tested-pwg-list<int:id>", views.tester_tested_pwg_list, name="tester-tested-pwg-list"),
    path("pwg-sublist<int:id>", views.pwg_sublist, name="pwg-sublist"),

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
    #tester URLs
    path("tester-home", views.tester_home, name='tester-home'),
    path("tester-test", views.tester_test, name='tester-test'),
    #User Urls
    # path("user-home", views.user_home, name='user-home'),
    path("user-user", views.user_user, name='user-user'),
    path("user-home", views.user_home, name='user-home'),

    # path("webAdmin_register", views.webAdmin_register.as_view(), name="webAdmin_register"),
    #password change
    path("password_change",views.password_change, name="password_change"),
    # path("reset_password/", auth_views.PasswordResetView.as_view(), name="reset_password"),
    # path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    # path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # ajax url
    path("validate_nickname", views.ajax_request, name="validate_nickname"),
    # to find username of Users
    path("find_username", views.find_username, name="find_username"),
    # delete
    path("delete", views.delete, name="delete"),
    # freeze
    path("freeze", views.freeze, name="freeze"),
    # Unfreeze
    path("unfreeze", views.unfreeze, name="unfreeze"),
    # transfer_pwg and pwgs
    path("transfer_pwgs", views.transfer_pwgs, name="transfer_pwgs"),
    # transfer_pwg and pwgs
    path("getback_pwgs", views.getback_pwgs, name="getback_pwgs"),
    # transfer_pwg and pwgs
    path("add-new", views.add_new, name="add-new"),
    # transfer_pwg and pwgs
    path("delete_multiple_user", views.delete_multiple_user, name="delete_multiple_user"),
    # transfer_pwg and pwgs
    path("freeze_multiple_user", views.freeze_multiple_user, name="freeze_multiple_user"),
    # change alias
    path("change_alias", views.change_alias, name="change_alias"),
    # get password history
    path("getpassword", views.getpassword, name="getpassword"),
    # get password history
    path("use_record", views.use_record, name="use_record"),
    # get password history
    path("assign", views.assign, name="assign"),
    # get password history
    path("getback", views.getback, name="getback"),
    # get password history
    path("assign_multiple", views.assign_multiple, name="assign_mulltiple"),
    # get password history
    path("tester_list", views.tester_list, name="tester_list"),

]
