from django.shortcuts import render, redirect
from .models import WebAdmin, Seller, Tester, WebUser, PWGServers, PWG, WebAdminLoginHistory, PasswordHistory, TransferPwgs, TransferPwg, PwgUseRecord
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.core import serializers
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import JsonResponse

# dictionary of num to text
num = {
    1:"One",2:"Two",3:"Three",4:"Four",5:"Five",6:"Six",7:"Seven",8:"Eight",9:"Nine",10:"Ten",11:"Eleven",12:"Twelve",13:"Thirteen",14:"Fourteen",15:"Fifteen",16:"Sixteen",17:"Seventeen",18:"Eighteen",19:"Nineteen",20:"Twenty"
}


# Create your views here.
def get_ip(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""

    return ip


#  login
def index(request):
    if request.method == 'POST':
        accType = request.POST['accType']
        password = request.POST['password']
        uname = request.POST['uname']

        user = auth.authenticate(username=uname, password=password)

        if user is not None:
            auth.login(request, user)
            # saving history
            ip = get_ip(request)
            if request.user_agent.device.family == "Other":
                device_name = request.user_agent.os.family
                device_name = device_name + " " + str(request.user_agent.os.version).replace(",","")
            else:
                device_name = request.user_agent.device.family

            history = WebAdminLoginHistory(user=user, login_IP=ip, device_name=device_name)
            history.save()

            if accType == 'admin':
                if WebAdmin.objects.filter(user=user).exists():
                    return redirect("admin-home")
                else:
                    messages.info(request, 'Invalid user id and password for Admin')
                    return redirect('/')

            elif accType == 'seller':
                if Seller.objects.filter(email=uname).exists():
                    return redirect("seller-home")
                else:
                    messages.info(request, 'Invalid user id and password for Seller')
                    return redirect('/')

            elif accType == 'tester':
                if Tester.objects.filter(email=uname).exists():
                    return render(request, 'tester/tester-home.html', {'num': [11, 23, 33, 42, 35, 67, 78, 49, 10]})
                else:
                    messages.info(request, 'Invalid user id and password for Tester')
                    return redirect('/')

            elif accType == 'user':
                if WebUser.objects.filter(email=uname).exists():
                    return redirect("user-home")
                else:
                    messages.info(request, 'Invalid user id and password for User')
                    return redirect('/')

        else:
            messages.info(request, 'Invalid user id and password')
            return redirect('/')

    else:
        return render(request, 'tesafe/index.html')


def register(request):
    if request.method == 'POST':
        accType = request.POST['accType']
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['uname']
        email = request.POST['email']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        file = request.FILES['file']

        # password checking

        if password1 == password2:
            # conditions to see if it already exists
            if User.objects.filter(username=uname):
                messages.error(request, "Username already exists! try again")
                return redirect('register')
            elif User.objects.filter(email=email):
                messages.error(request, "Email already exists! try again")
                return redirect('register')
            else:
                # fetching device info
                if request.user_agent.device.family == "Other":
                    device_name = request.user_agent.os.family
                    device_name = device_name + " " + str(request.user_agent.os.version).replace(",", "")
                else:
                    device_name = request.user_agent.device.family

                # if it is admin
                if accType == 'admin':
                    user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email, password=password1)
                    user.save()

                    # creating password history
                    passHistory = PasswordHistory(user=user, device_name=device_name,last_pass=password1)
                    passHistory.save()

                    webAdmin = WebAdmin(user=user, first_name=fname, last_name=lname, email=email, phone=phone)
                    webAdmin.save()

                    return render(request, 'tesafe/admin-home.html')

                # if it is seller
                elif accType == 'seller':
                    user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email, password=password1)
                    user.save()

                    # creating password history
                    passHistory = PasswordHistory(user=user, device_name=device_name, last_pass=password1)
                    passHistory.save()

                    seller = Seller(user=user, first_name=fname, last_name=lname, email=email, phone=phone, profile_pic=file, alias=uname)
                    seller.save()

                    return render(request, 'seller/seller-home.html')

                # if it is tester
                elif accType == 'tester':
                    user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email,
                                                    password=password1)
                    user.save()

                    # creating password history
                    passHistory = PasswordHistory(user=user, device_name=device_name, last_pass=password1)
                    passHistory.save()

                    tester = Tester(user=user, first_name=fname, last_name=lname, email=email, phone=phone, profile_pic=file, alias=uname)
                    tester.save()

                    return render(request, 'tester/tester-home.html')

                # if it is user
                elif accType == 'user':
                    user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email,
                                                    password=password1)
                    user.save()

                    # creating password history
                    passHistory = PasswordHistory(user=user, device_name=device_name, last_pass=password1)
                    passHistory.save()

                    webUser = WebUser(user=user, first_name=fname, last_name=lname, email=email, phone=phone, profile_pic=file, alias=uname)
                    webUser.save()

                    return render(request, 'user/user-home.html')
        else:
            messages.error(request, "Password do not match! try again")
            return redirect('register')

    return render(request, 'tesafe/register.html')


def logout(request):
    auth.logout(request)
    messages.info(request,"successfully logged out")
    return redirect("/")


def get_current_users(obj):
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list

    return obj.objects.filter(id__in=user_id_list)


def admin_home(request):
    seller_count = Seller.objects.all().count()
    tester_count = Tester.objects.all().count()
    web_user_count = WebUser.objects.all().count()
    PWGS_count = PWGServers.objects.all().count()
    queryset_seller = get_current_users(Seller)
    queryset_tester = get_current_users(Tester)
    queryset_web_user = get_current_users(WebUser)
    queryset_PWGs = get_current_users(PWGServers)
    history_count = WebAdminLoginHistory.objects.filter(user=request.user).count()
    params = {
        'seller_count': seller_count,
        'tester_count': tester_count,
        'web_user_count': web_user_count,
        'PWGs_count': PWGS_count,
        'seller_online': queryset_seller.count(),
        'seller_offline': seller_count - queryset_seller.count(),
        'tester_online': queryset_tester.count(),
        'tester_offline': tester_count - queryset_tester.count(),
        'web_user_online': queryset_web_user.count(),
        'web_user_offline': web_user_count - queryset_web_user.count(),
        'PWGs_offline': PWGS_count - queryset_PWGs.count(),
        'PWGs_online': queryset_PWGs.count(),
        'history': WebAdminLoginHistory.objects.filter(user=request.user).order_by('-login_date'),
        'history_count': history_count,
        'password_history': PasswordHistory.objects.filter(user=request.user).order_by('-login_date')
    }
    return render(request, 'tesafe/admin-home.html', params)


def admin_seller(request):
    seller = Seller.objects.all()
    param = {
        'seller': seller,
    }
    return render(request, 'tesafe/admin-seller.html', param)


def admin_tester(request):
    tester = Tester.objects.all()
    param = {
        'tester': tester,
    }

    return render(request, 'tesafe/admin-tester.html', param)


def admin_info_server(request):
    pwgs = PWGServers.objects.all()
    pwg = PWG.objects.all()
    count_pwgs = pwgs.count()
    count_pwg = pwg.count()
    pwgs_active = get_current_users(PWGServers).count()
    pwg_active = get_current_users(PWG).count()
    param = {
        'pwgs': pwgs,
        'pwg': pwg,
        'total_pwgs': count_pwgs,
        'total_pwgs_online': pwgs_active,
        'total_pwgs_offline': count_pwgs - pwgs_active,
        'total_pwg': count_pwg,
        'total_pwg_online': pwg_active,
        'total_pwg_offline': count_pwg - pwg_active,
    }
    return render(request, 'tesafe/admin-info-server.html', param)


# never used
# def register_next(request):
#     if request.method == 'POST':
#         accType = request.POST['accType']
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         uname = request.POST['uname']
#         email = request.POST['email']
#         phone = request.POST['phone']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']
#
#         if accType == 'admin':
#             if password1 == password2:
#                 user = User.objects.create_user(username=uname, first_name=fname, last_name=lname, email=email,
#                                                 password=password1, is_webAdmin=True)
#                 user.save()
#
#                 webAdmin = WebAdmin(name=fname, phone=phone, email=email)
#                 webAdmin.save()
#                 msg = messages.info("Account successfully created!")
#                 return render(request, 'tesafe/admin-page.html', {'msg': msg})
#
#             else:
#                 msg = messages.error(request, "Password do not match! try again")
#                 return render(request, 'tesafe/admin-page.html', {'msg': msg})
#
#     return render(request, 'tesafe/admin-seller.html', {})


def seller_home(request):
    count = 0
    user_online = 0
    user_offline = 0
    seller_user = request.user
    seller = seller_user.id
    seller = Seller.objects.get(user=seller)
    if TransferPwg.objects.filter(user=seller_user).exists():
        pwg = TransferPwg.objects.filter(user=seller_user)
        count = pwg.count()
    if seller.user_count != 0:
        user_online = WebUser.objects.filter(associated_with=seller)
        user_offline = WebUser.objects.filter(associated_with=seller)

    history_count = WebAdminLoginHistory.objects.filter(user=request.user).count()
    history = WebAdminLoginHistory.objects.filter(user=request.user).order_by('-login_date')

    param = {
        "seller": seller,
        "pwgs": count,
        "pwg_online": count,
        "pwg_offline": count - get_current_users(PWG).count(),
        "user_online": user_online,
        "user_offline": user_offline,
        "history_count": history_count,
        "history": history,
        'password_history': PasswordHistory.objects.filter(user=request.user).order_by('-login_date'),

    }
    return render(request, 'seller/seller-home.html', param)


def seller_user(request):
    seller = request.user
    user = User.objects.get(email=seller)
    seller = Seller.objects.get(user=user.id)

    if WebUser.objects.filter(associated_with=seller.id).exists():
        web_users = WebUser.objects.filter(associated_with=seller.id)
    else:
        web_users = None

    param = {
        "users": web_users,
        "id": seller.id,
    }
    return render(request, 'seller/seller-user.html', param)


def seller_pwg(request):
    return render(request, 'seller/seller-pwg.html', {'num': [11,23,33,42,35,67,78,49,10]})


def transfer(request, id):
    user = User.objects.get(id=id)
    pwgserver = PWGServers.objects.all()
    pwg = PWG.objects.all()
    param = {
        "name": "Transfer Tested PWG to Seller "+user.first_name + " " + user.last_name,
        "pwgserver": pwgserver,
        "pwg": pwg,
        "num": num,
        "id": id
    }
    return render(request, 'tesafe/transfer.html', param)


def tester_getback(request, id):
    if User.objects.filter(id=id).exists():
        user = User.objects.get(id=id)
        list1 = []
        transferred_pwg = TransferPwg.objects.filter(user=id)

        if transferred_pwg is None:
            transferred_pwg = TransferPwg.objects.all()

        for obj in transferred_pwg:
            list1.append(obj.pwgs_owner)

        list1 = set(list1)

        param = {
            'trans_pwg': transferred_pwg,
            'servers': list1,
            "name": user.first_name + " " + user.last_name,
            "id": id,
        }
        return render(request, 'tesafe/tester-getback.html', param)
    else:
        messages.error(request, "This Tester has no PWG")
        return redirect('admin-tester')


def tester_tested_pwg_list(request, id):
    user = User.objects.get(id=id)
    pwgserver = PWGServers.objects.all()
    pwg = PWG.objects.all()
    param = {
        "name": "Transfer PWG to Tester " + user.first_name + " " + user.last_name,
        "pwgserver": pwgserver,
        "pwg": pwg,
        "num": num,
        "id": id
    }
    return render(request, 'tesafe/tester-tested-pwg-list.html', param)


def pwg_sublist(request, id):
    if PWG.objects.filter(owned_by=id).exists():
        pwg = PWG.objects.filter(owned_by=id)
        name = pwg[0].owned_by
        param = {
            'pwg': pwg,
            'name': name,
            'id': id,
        }
        return render(request, 'tesafe/pwg-sublist.html', param)
    else:
        messages.error(request, "This PWG Server has no PWG")
        return redirect("admin-info-server")


def transfer_seller(request):
    return render(request, 'seller/transfer-seller.html')


def transfer_seller_pwg(request):
    return render(request, 'seller/transfer-seller-pwg.html')


def seller_authorized(request):
    return render(request, 'seller/seller-authorized.html')


def seller_authorized_pwg(request):
    return render(request, 'seller/seller-authorized-pwg.html')


def seller_shared_pwg(request):
    return render(request, 'seller/seller-shared-pwg.html')


def seller_deauthorized_pwg(request):
    return render(request, 'seller/seller-deauthorized-pwg.html')


def seller_shared(request):
    return render(request, 'seller/seller-shared.html')


def seller_deshared_pwg(request):
    return render(request, 'seller/seller-deshared-pwg.html')


def seller_pwg_transfer(request):
    return render(request, 'seller/seller-pwg-transfer.html')


def tester_home(request):
    return render(request, 'tester/tester-home.html')


def tester_test(request):
    return render(request, 'tester/tester-test.html')


def user_user(request):
    return render(request, 'user/user-user.html')


def user_home(request):
    return render(request, 'user/user-home.html')


# TODOs
def password_change(request):
    if request.method == "POST":
        old_email = request.POST['old_password']
        new_email = request.POST['new_password']
        new_conf_email = request.POST['new_conf_password']
        accType = request.POST['accType']

        if old_email == new_conf_email or old_email == new_email:
            messages.info(request, "Old and new Password are Same, use different!")
            if accType == "seller":
                return redirect("seller-home")
            elif accType == "admin":
                return redirect("admin-home")

        elif new_conf_email == new_email:
            # creating password history
            u = User.objects.get(username=request.user)
            # getting device info
            if request.user_agent.device.family == "Other":
                device_name = request.user_agent.os.family
                device_name = device_name + " " + str(request.user_agent.os.version).replace(",", "")
            else:
                device_name = request.user_agent.device.family

            if u.check_password(old_email):
                passHistory = PasswordHistory(user=request.user, device_name=device_name, last_pass=old_email)
                passHistory.save()

                u.set_password(new_email)
                u.save()
                messages.info(request, "Successfully changed your password")
                return redirect("/")
            else:
                messages.info(request, "Wrong Old Password!")
                if accType == "seller":
                    return redirect("seller-home")
                elif accType == "admin":
                    return redirect("admin-home")
        else:
            messages.info(request, "New Password does not match!")
            if accType == "seller":
                return redirect("seller-home")
            elif accType == "admin":
                return redirect("admin-home")


    else:
        return render(request, "index.html")


# to find username
def ajax_request(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the history from the database
        pk = request.GET.get("pk", None)
        accType = request.GET.get("accType", None)
        # check for the pk in the database.

        if WebAdminLoginHistory.objects.filter(user_id=pk).exists():
            # if history found return history
            history = WebAdminLoginHistory.objects.filter(user_id=pk)
            history_json = serializers.serialize('json', history)

            return HttpResponse(history_json, content_type='application/json')
        else:
            # if history not found, then return true
            return JsonResponse({"history": False}, status=200)

    return JsonResponse({}, status=400)


def find_username(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the history from the database
        pk = request.GET.get("pk", None)
        accType = request.GET.get("accType", None)
        # check for the pk in the database.
        if accType == "seller" or accType == "tester":
            if User.objects.filter(pk=pk).exists():
                name = User.objects.get(pk=pk)
                name1 = name.first_name
                return JsonResponse({"name": name1}, status=200)
            else:
                # if name not found, then return true
                return JsonResponse({"name": False}, status=200)

        elif accType == 'pwg':
            if PWG.objects.filter(id=pk).exists():
                pwg = PWG.objects.get(id=pk)
                name = pwg.alias
                return JsonResponse({"name": name}, status=200)
            else:
                # if name not found, then return true
                return JsonResponse({"name": False}, status=200)

    return JsonResponse({}, status=400)


def delete(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the history from the database
        pk = request.GET.get("pk", None)
        accType = request.GET.get("accType", None)

        if accType == "seller" or accType == "tester" or accType == "user":
            # check for the pk in the database.
            if User.objects.filter(id=pk).exists():
                my_object = User.objects.get(id=pk)
                name = my_object.first_name
                name = "{} has been successfully deleted".format(name)
                my_object.delete()
                return JsonResponse({"msg": name}, status=200)
            else:
                # if name not found, then return msg
                return JsonResponse({"msg": False}, status=200)

        elif accType == "pwgs":
            if PWGServers.objects.filter(id=pk).exists():
                pwgs = PWGServers.objects.get(id=pk)
                name = pwgs.alias
                print(name)
                name = "{} has been successfully deleted".format(name)
                pwgs.delete()

                return JsonResponse({"msg": name}, status=200)
            else:
                # if name not found, then return msg
                return JsonResponse({"msg": False}, status=200)

    return JsonResponse({}, status=400)


def freeze(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the history from the database
        pk = request.GET.get("pk", None)
        user = request.GET.get("user", None)
        if user == "seller":
            # check for the pk in the database.
            if Seller.objects.filter(id=pk).exists():
                my_object = Seller.objects.get(id=pk)
                my_object.is_freeze = True
                name = my_object.alias
                my_object.save()
                name = "{} has been successfully freezed".format(name)
                return JsonResponse({"msg": name}, status=200)
            else:
                # if name not found, then return msg
                return JsonResponse({"msg": False}, status=200)

        elif user == "tester":
            # check for the pk in the database.
            if Tester.objects.filter(id=pk).exists():
                my_object = Tester.objects.get(id=pk)
                my_object.is_freeze = True
                name = my_object.alias
                my_object.save()
                name = "{} has been successfully freezed".format(name)
                return JsonResponse({"msg": name}, status=200)
            else:
                # if name not found, then return msg
                return JsonResponse({"msg": False}, status=200)
        elif user == "pwg":
            # check for the pk in the database.
            if PWG.objects.filter(id=pk).exists():
                my_object = PWG.objects.get(id=pk)
                my_object.is_freeze = True
                name = my_object.alias
                my_object.save()
                name = "{} has been successfully freezed".format(name)
                return JsonResponse({"msg": name}, status=200)
            else:
                # if name not found, then return msg
                return JsonResponse({"msg": False}, status=200)

        elif user == "user":
            # check for the pk in the database.
            if WebUser.objects.filter(id=pk).exists():
                my_object = WebUser.objects.get(id=pk)
                my_object.is_freeze = True
                name = my_object.alias
                my_object.save()
                name = "{} has been successfully freezed".format(name)
                return JsonResponse({"msg": name}, status=200)
            else:
                # if name not found, then return msg
                return JsonResponse({"msg": False}, status=200)

    return JsonResponse({}, status=400)


def unfreeze(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the history from the database
        pk = request.GET.get("pk", None)
        user = request.GET.get("user", None)
        if user == "seller":
        # check for the pk in the database.
            if Seller.objects.filter(id=pk).exists():
                my_object = Seller.objects.get(id=pk)
                my_object.is_freeze = False
                name = my_object.alias
                my_object.save()
                name = "{} has been successfully unfreezed".format(name)
                return JsonResponse({"msg": name}, status=200)
            else:
                # if name not found, then return msg
                return JsonResponse({"msg": False}, status=200)

        elif user == "tester":
            # check for the pk in the database.
            if Tester.objects.filter(id=pk).exists():
                my_object = Tester.objects.get(id=pk)
                my_object.is_freeze = False
                name = my_object.alias
                my_object.save()
                name = "{} has been successfully unfreezed".format(name)
                return JsonResponse({"msg": name}, status=200)
            else:
                # if name not found, then return msg
                return JsonResponse({"msg": False}, status=200)
        elif user == "pwg":
            # check for the pk in the database.
            if PWG.objects.filter(id=pk).exists():
                my_object = PWG.objects.get(id=pk)
                my_object.is_freeze = False
                name = my_object.alias
                my_object.save()
                name = "{} has been successfully unfreezed".format(name)
                print(name)
                return JsonResponse({"msg": name}, status=200)
            else:
                # if name not found, then return msg
                return JsonResponse({"msg": False}, status=200)

        elif user == "user":
            # check for the pk in the database.
            if WebUser.objects.filter(id=pk).exists():
                my_object = WebUser.objects.get(id=pk)
                my_object.is_freeze = False
                name = my_object.alias
                my_object.save()
                name = "{} has been successfully unfreezed".format(name)
                return JsonResponse({"msg": name}, status=200)
            else:
                # if name not found, then return msg
                return JsonResponse({"msg": False}, status=200)

    return JsonResponse({}, status=400)


def delete_multiple_user(request):
    # request's method  should be POST
    if request.method == "POST":
        sellers = []
        # fetch the data from the request
        values = request.POST.get("values", None)
        accType = request.POST.get("accType", None)

        # print(values)
        if accType == "seller":
            for i in values:
                if Seller.objects.filter(id=i).exists():
                    seller = Seller.objects.get(id=i)
                    id_user = seller.user_id
                    seller = User.objects.get(id=id_user)
                    seller.delete()

            return redirect('admin-seller')

        elif accType == "tester":
            for i in values:
                if Tester.objects.filter(id=i).exists():
                    tester = Tester.objects.get(id=i)
                    id_user = tester.user_id
                    tester = User.objects.get(id=id_user)
                    tester.delete()

            return redirect('admin-tester')
        elif accType == "pwgs":
            for i in values:
                if PWGServers.objects.filter(id=i).exists():
                    pwgs = PWGServers.objects.get(id=i)
                    pwgs.delete()

            return redirect('admin-info-server')

    return redirect('admin-home')


def transfer_pwgs(request):
    # request's method  should be POST
    if request.method == "POST":
        pwg = []
        pwg_server = []
        flag = False
        # fetch the data from the database
        values = request.POST.get("values", None)
        pk = request.POST.get("user_pk", None)
        accType = request.POST.get("accType", None)

        current_user = User.objects.get(pk=pk)
        # separating pk of PWG Server and PWG
        # print("values ",values)
        for i in range(len(values)):
            if values[i] == 's':
                pwg_server.append(values[i+1])
                flag = True
            elif values[i] == ',':
                pass
            else:
                if flag:
                    flag = False
                else:
                    pwg.append(values[i])

        # making it unique
        pwg = set(pwg)
        pwg = list(pwg)

        if len(pwg) != 0:
            for i in pwg:
                pwg_object = PWG.objects.get(id=i)
                pwgs_id = pwg_object.owned_by
                pwg_object.transfer_to = current_user

                if accType == "seller":
                    pwg_object.location = "S"
                    pwg_object.save()
                elif accType == "tester":
                    pwg_object.location = "T"
                    pwg_object.save()

                transfer = TransferPwg(pwg_owner=pwg_object, pwgs_owner=pwgs_id, user=current_user)
                transfer.save()

        if accType == "seller":
            return redirect('admin-seller')
        elif accType == "tester":
            return redirect('admin-tester')
    return redirect('admin-seller')


def getback_pwgs(request):
    # request's method  should be POST
    if request.method == "POST":
        pwg = []
        pwg_server = []
        flag = False
        # fetch the data from the database
        values = request.POST.get("values", None)
        pk = request.POST.get("user_pk", None)

        current_user = User.objects.get(pk=pk)
        # separating pk of PWG Server and PWG
        # print("values ",values)
        for i in range(len(values)):
            if values[i] == 's':
                pwg_server.append(values[i+1])
                flag = True
            elif values[i] == ',':
                pass
            else:
                if flag:
                    flag = False
                else:
                    pwg.append(values[i])

        # making it unique
        print(pwg)
        print(pwg_server)
        pwg = set(pwg)
        pwg = list(pwg)

        if len(pwg) != 0:
            for i in pwg:
                trans_pwg = TransferPwg.objects.get(pwg_owner=i)
                trans_pwg.delete()

        return redirect('admin-tester')
    return redirect('admin-tester')


def add_new(request):
    if request.method == 'POST':
        fname = request.POST.get('fname', None)
        lname = request.POST.get('lname', None)
        name = str(request.POST.get('name', None))
        alias = request.POST['alias']
        seller_id = request.POST.get('seller_id', None)
        email = request.POST['email']
        number = request.POST.get('number', None)
        password = request.POST['password']
        accType = request.POST['accType']

        if User.objects.filter(email=email).exists():
            messages.info(request, "Email already exists, try again!")
            if accType == "pwgs":
                return redirect("admin-info-server")
            elif accType == "seller":
                return redirect("admin-seller")
            elif accType == "tester":
                return redirect("admin-tester")

        if accType != "pwgs":
            # creating user
            user = User.objects.create_user(username=email, email=email, first_name=fname, last_name=lname, password=password)
            user.save()

        # creating seller account
        if accType == "seller":
            seller = Seller(user=user, first_name=fname, last_name=lname, alias=alias, email=email, phone=number)
            seller.save()
            messages.info(request, "Successfully Account Created!")
            return redirect("admin-seller")

        # creating tester account
        elif accType == "tester":
            tester = Tester(user=user, first_name=fname, last_name=lname, alias=alias, email=email, phone=number)
            tester.save()
            messages.info(request, "Successfully Account Created!")
            return redirect("admin-tester")

        # creating PWGS account
        elif accType == "pwgs":
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()
            pwgs = PWGServers(name=name, alias=alias, email=email, password=password, pwg_count=0, user=user)
            pwgs.save()
            messages.info(request, "Successfully Account Created!")
            return redirect("admin-info-server")
        # creating PWGS account
        elif accType == "user":
            if user is not None:
                seller_id = Seller.objects.get(id=seller_id)
                user_obj = WebUser(user=user, first_name=fname, last_name=lname, email=email, phone=number, alias=alias, associated_with=seller_id)
                user_obj.save()
                messages.info(request, "Successfully Account Created!")
                return redirect("seller-user")
            else:
                messages.info(request, "Something went wrong, try again")
                return redirect("seller-user")

    else:
        return redirect("admin-home")


def freeze_multiple_user(request):
    # request's method  should be POST
    if request.method == "POST":
        sellers = []
        # fetch the data from the request
        values = request.POST.get("freeze_values", None)
        accType = request.POST.get("accType", None)
        pk = request.POST.get("pk", None)

        # print(values)
        if accType == "seller":
            for i in values:
                if Seller.objects.filter(id=i).exists():
                    seller = Seller.objects.get(id=i)
                    seller.is_freeze = True
                    seller.save()

            return redirect('admin-seller')

        elif accType == "tester":
            for i in values:
                if Tester.objects.filter(id=i).exists():
                    tester = Tester.objects.get(id=i)
                    tester.is_freeze = True
                    tester.save()

            return redirect('admin-tester')
        elif accType == "pwg":
            for i in values:
                if PWG.objects.filter(id=i).exists():
                    pwg = PWG.objects.get(id=i)
                    pwg.is_freeze = True
                    pwg.save()
            if pk:
                return redirect('pwg-sublist', id=int(pk))
            else:
                return redirect('admin-info-server')
    return redirect('admin-home')


def change_alias(request):
    if request.method == "POST":
        alias = request.POST.get('alias')
        alias_id = request.POST.get('alias_id')
        accType = request.POST.get('accType')
        alias_conf = request.POST.get('alias_conf', None)

        if accType == "pwgs":
            if PWGServers.objects.filter(id=alias_id).exists():
                pwgs = PWGServers.objects.get(id=alias_id)
                pwgs.alias = alias
                pwgs.save()

                return redirect("admin-info-server")
            else:
                messages.error(request, "PWG Server Does not exists")
                return redirect("admin-info-server")

        if accType == "seller":
            if alias_conf == alias:
                if User.objects.filter(id=alias_id).exists():
                    user_obj = User.objects.get(id=alias_id)
                    print(user_obj)
                    return redirect("seller-home")
                else:
                    messages.error(request, "Seller does not exists")
                    return redirect("seller-home")
            else:
                messages.error(request, "Alias name does not match! try again")
                return redirect("seller-home")

    else:
        messages.info(request, "Something went wrong! try again")
        return redirect("/")


def getpassword(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the history from the database
        pk = request.GET.get("pk", None)
        if PasswordHistory.objects.filter(user=pk).exists():
            history = PasswordHistory.objects.filter(user=pk)
            history_json = serializers.serialize('json', history)

            return HttpResponse(history_json, content_type='application/json')
        else:
            return JsonResponse({"history": False}, status=200)
    else:
        return JsonResponse({}, status=200)


def use_record(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        pk = request.GET.get("pk", None)
        if PwgUseRecord.objects.filter(id=pk).exists():
            use_record = PwgUseRecord.objects.filter(id=pk)
            use_record_json = serializers.serialize('json', use_record)

            return HttpResponse(use_record_json, content_type='application/json')
        else:
            return JsonResponse({'history': False}, status=200)
    else:
        return JsonResponse({}, status=200)


def assign(request):
    # request should be ajax and method should be GET.
    if request.method == "POST":
        pk = request.POST.get("pk", None)
        tester_ids = request.POST.get("tester_ids", None)

        for i in tester_ids:
            if i == ",":
                pass
            else:
                pwg = PWG.objects.get(id=pk)
                pwgs = pwg.owned_by
                tester = Tester.objects.get(id=i)
                user = User.objects.get(email=tester.email)
                transfer_pwg = TransferPwg(pwg_owner=pwg, pwgs_owner=pwgs, user=user)
                transfer_pwg.save()
                pwg.location = "T"
                pwg.transfer_to = user
                pwg.save()

        return redirect("pwg-sublist", id=pwgs.id)
    else:
        return JsonResponse({}, status=200)


def assign_multiple(request):
    # request should be ajax and method should be GET.
    if request.method == "POST":
        pk = request.POST.get("pk", None)
        tester_ids = request.POST.get("tester_ids", None)

        for i in tester_ids:
            tester = Tester.objects.get(id=i)
            user = User.objects.get(email=tester.email)
            if i == ",":
                pass
            else:
                for j in pk:
                    if j == ",":
                        pass
                    else:
                        pwg = PWG.objects.get(id=j)
                        pwgs = pwg.owned_by
                        transfer_pwg = TransferPwg(pwg_owner=pwg, pwgs_owner=pwgs, user=user)
                        transfer_pwg.save()
                        pwg.location = "T"
                        pwg.transfer_to = user
                        pwg.save()

        return redirect("pwg-sublist", id=pwgs.id)
    else:
        return JsonResponse({}, status=200)


def tester_list(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        tester = Tester.objects.all()
        tester_json = serializers.serialize('json', tester)

        return HttpResponse(tester_json, content_type='application/json')
    else:
        return JsonResponse({"data": False}, status=200)


def getback(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        pk = request.GET.get("pk", None)
        if PWG.objects.filter(id=pk).exists():
            pwg = PWG.objects.get(id=pk)
            if pwg.transfer_to:
                name = "{} has been successfully taken back from Tester".format(pwg.alias)
            else:
                name = "{} has been successfully taken back from Tester {}".format(pwg.alias,
                                                                                   pwg.transfer_to)
            pwg.location = "A"
            usr = User.objects.get(is_superuser=True)
            pwg.transfer_to = usr
            pwg.save()

            return JsonResponse({"msg": name}, status=200)
        else:
            return JsonResponse({"msg": False}, status=200)
    else:
        return JsonResponse({}, status=200)
