from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .api import MessageModelViewSet, UserModelViewSet

# for messages routing
router = DefaultRouter()
router.register(r'message', MessageModelViewSet, basename='message-api')
router.register(r'user', UserModelViewSet, basename='user-api')

urlpatterns = [
    # admin urls
    path("", views.index, name="index"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("admin-home", views.admin_home, name="admin-home"),
    path("transfer<int:id>", views.transfer, name="transfer"),
    path("admin-seller", views.admin_seller, name="admin-seller"),
    path("assist_admin", views.assist_admin, name="assist_admin"),
    path("admin-tester", views.admin_tester, name="admin-tester"),
    path("pwg-sublist<int:id>", views.pwg_sublist, name="pwg-sublist"),
    path("tester-getback<int:id>", views.tester_getback, name="tester-getback"),
    path("admin-info-server", views.admin_info_server, name="admin-info-server"),
    path("tester-tested-pwg-list<int:id>", views.tester_tested_pwg_list, name="tester-tested-pwg-list"),

    # seller PWG
    path("seller-pwg", views.seller_pwg, name="seller-pwg"),
    path("seller-home", views.seller_home, name="seller-home"),
    path("seller-user", views.seller_user, name="seller-user"),
    path("seller-shared<int:pk>", views.seller_shared, name="seller-shared"),
    path("seller-shared-pwg", views.seller_shared_pwg, name="seller-shared-pwg"),
    path("transfer-seller<int:pk>", views.transfer_seller, name="transfer-seller"),
    path("transfer-seller-pwg", views.transfer_seller_pwg, name="transfer-seller-pwg"),
    path("seller-deshared-pwg", views.seller_deshared_pwg, name="seller-deshared-pwg"),
    path("seller-deauthorize-pwg", views.seller_deauthorize_pwg, name="seller-deauthorize-pwg"),
    path("seller-authorized<int:pk>", views.seller_authorized, name="seller-authorized"),
    path("seller-authorized-pwg", views.seller_authorized_pwg, name="seller-authorized-pwg"),

    # tester URLs
    path("tester-home", views.tester_home, name='tester-home'),
    path("tester-test", views.tester_test, name='tester-test'),
    # to make pwg fail
    path("fail", views.fail, name='fail'),
    # to make pwg pass
    path("pass_pwg", views.pass_pwg, name='pass_pwg'),

    # User Urls
    path("user-user", views.user_user, name='user-user'),
    path("user-home", views.user_home, name='user-home'),
    path("user_list", views.user_list, name='user_list'),
    path("share_transfer_multiple", views.share_transfer_multiple, name='share_transfer_multiple'),
    path("user_deauthorize_pwg", views.user_deauthorize_pwg, name='user_deauthorize_pwg'),
    path("user-deshared-pwg", views.user_deshared_pwg, name='user-deshared-pwg'),

    # password reset functionality
    path("request-reset-link", views.RequestPasswordResetEmail.as_view(), name="request-reset-link"),
    path("set-new-password/<uidb64>/<token>", views.CompletePasswordReset.as_view(), name="reset-user-password"),

    # Payment URLs
    path("simple_checkout", views.simple_checkout, name="simple_checkout"),
    # delete
    path("delete", views.delete, name="delete"),
    # freeze
    path("freeze", views.freeze, name="freeze"),
    # Unfreeze
    path("unfreeze", views.unfreeze, name="unfreeze"),
    # to find username of Users
    path("find_username", views.find_username, name="find_username"),
    # password change
    path("password_change",views.password_change, name="password_change"),
    # ajax url
    path("validate_nickname", views.ajax_request, name="validate_nickname"),
    # transfer_pwg and pwgs
    path("Transfer_pwgs", views.transfer_pwgs, name="Transfer_pwgs"),
    # authorize pwgs
    path("Authorize_pwgs", views.authorize_pwgs, name="Authorize_pwgs"),
    # authorize pwgs
    path("authorize_multiple_pwgs", views.authorize_multiple_pwgs, name="authorize_multiple_pwgs"),
    # De-authorize pwgs
    path("deauthorize", views.deauthorize, name="deauthorize"),
    # Share pwgs
    path("share_pwgs", views.share_pwgs, name="share_pwgs"),
    # Share multiple pwgs
    path("share_multiple_pwgs", views.share_multiple_pwgs, name="share_multiple_pwgs"),
    # De-authorize pwgs
    path("deshare", views.deshare, name="deshare"),
    # De-share multiple pwgs
    path("deshare_multiple_pwgs", views.deshare_multiple_pwgs, name="deshare_multiple_pwgs"),
    # De-authorize multiple pwgs
    path("deauthorize_multiple_pwgs", views.deauthorize_multiple_pwgs, name="deauthorize_multiple_pwgs"),
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
    # get all tester objects
    path("tester_list", views.tester_list, name="tester_list"),
    # get all seller objects
    path("seller_list", views.seller_list, name="seller_list"),
    # get system name
    path("unique_name", views.system_name, name="unique_name"),
    # delete for a particular module
    path("delete_temp", views.delete_temp, name="delete_temp"),
    # return PWG to Admin
    path('return-pwg', views.return_pwg, name='return-pwg'),
    # transfer multiple pwgs to one users
    path('transfer_pwg_multiple_users', views.transfer_pwg_multiple_users, name='transfer_pwg_multiple_users'),
    # to show testing history
    path('testing_history', views.testing_history, name='testing_history'),
    # to test again the PWG
    path('retest', views.retest, name='retest'),
    # custom password change
    path('custom_reset', views.custom_reset, name='custom_reset'),
    # to save pwg access password
    path('passText', views.passtext, name='passText'),
    # to check if the user is laready exists
    path('destination', views.destination, name='destination'),
    path('accounts/login/', views.index, name='login'),
    # to mark the notifications as read
    path('mark_read', views.mark_read, name='mark_read'),
    # to get PWG date when it was get from admin
    path('get_from', views.get_from, name='get_from'),
    # to check password
    path('check_password', views.check_password, name='check_password'),

    # Messages route to API
    path(r'api/v1/', include(router.urls)),
    # for single user chat
    path('chat', views.custom_chat, name='chat'),
    # for multiple user chat
    path('broadcast', views.broadcast, name='broadcast'),
    # for broadcast from admin account
    path('broadcast-admin', views.broadcast_admin, name='broadcast-admin'),
    # chat multiple
    path('chat_multiple', views.chat_multiple, name='chat_multiple'),
    # to get chat history
    path('chat_history', views.chat_history, name='chat_history'),
]

# How to get an array in Django posted via Ajax => see in broadcast view
