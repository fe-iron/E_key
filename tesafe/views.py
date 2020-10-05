from django.shortcuts import render, redirect
from .models import WebAdmin, Seller, Tester, WebUser, PWGServers, PWG, WebAdminLoginHistory, PasswordHistory, \
    TransferPwgs, TransferPwg, PwgUseRecord, SystemName, Authorize, Share, PWGHistory
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.core import serializers
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import JsonResponse
from .utils import unique_name
from django.db.models import Q
import json


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
                    return redirect('tester-home')
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
        'history': WebAdminLoginHistory.objects.filter(user=request.user).order_by('-login_time'),
        'history_count': history_count,
        'password_history': PasswordHistory.objects.filter(user=request.user).order_by('-login_time')
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


def seller_home(request):
    count = 0
    user_online = 0
    user_offline = 0
    seller_user = request.user
    seller = seller_user.id
    seller = Seller.objects.get(user=seller)
    if PWG.objects.filter(transfer_to=seller_user).exists():
        pwg = PWG.objects.filter(transfer_to=seller_user)
        count = pwg.count()

    history_count = WebAdminLoginHistory.objects.filter(user=request.user).count()
    history = WebAdminLoginHistory.objects.filter(user=request.user).order_by('-login_time')

    param = {
        "seller": seller,
        "pwgs": count,
        "pwg_online": get_current_users(PWG).count(),
        "pwg_offline": count - get_current_users(PWG).count(),
        "user_online": seller.user_count,
        "user_offline": 0,
        "history_count": history_count,
        "history": history,
        'password_history': PasswordHistory.objects.filter(user=request.user).order_by('-login_time'),

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
        "unique_name": unique_name("S", '001'),
    }
    return render(request, 'seller/seller-user.html', param)


def seller_pwg(request):
    pwgserver = []
    pwgserver1 = []
    user = request.user
    pwg = PWG.objects.filter(Q(transfer_to=user) | Q(sold_from=user))
    for i in pwg:
        if i.is_authorized or i.is_shared or i.sold_from:
            pwgs = i.owned_by
            try:
                pwgserver.index(pwgs)

            except ValueError as ve:
                pwgserver.append(pwgs)
        else:
            pwgs = i.owned_by
            pwgserver1.append(pwgs)
    param = {
        "pwgserver_occupied": pwgserver,
        "pwgserver_unoccupied": pwgserver1,
        "pwg": pwg,
        "num": num,
    }
    return render(request, 'seller/seller-pwg.html', param)


def transfer(request, id):
    user = User.objects.get(id=id)
    pwgserver = PWGServers.objects.all()
    pwg = PWG.objects.all()
    param = {
        "name": "Transfer PWG to Seller "+user.first_name + " " + user.last_name,
        "username": user.first_name + " " + user.last_name,
        "pwgserver": pwgserver,
        "pwg": pwg,
        "num": num,
        "id": id,
        "accType": "admin",
        "target": "seller",
        "action": "Transfer",
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


def transfer_seller(request, pk):
    user = User.objects.get(id=pk)
    pwgserver = PWGServers.objects.all()
    pwg = PWG.objects.all()
    param = {
        "name": "Transfer PWG to User " + user.first_name + " " + user.last_name,
        "username": user.first_name + " " + user.last_name,
        "pwgserver": pwgserver,
        "pwg": pwg,
        "num": num,
        "id": pk,
        "accType": "seller",
        "target": "user",
        "action": "Transfer",
    }
    return render(request, 'tesafe/transfer.html', param)


def transfer_seller_pwg(request):
    if request.method == "POST":
        ids = request.POST['pwg_ids']
        name = ' '
        pwg_ids = []
        for id in ids:
            if id == ",":
                pass
            elif id == " ":
                pass
            else:
                pwg = PWG.objects.get(id=id)
                name = " " + pwg.alias + ", " + name
                pwg_ids.append(pwg.id)

        seller = request.user
        user = User.objects.get(email=seller)
        seller = Seller.objects.get(user=user.id)

        if WebUser.objects.filter(associated_with=seller.id).exists():
            web_users = WebUser.objects.filter(associated_with=seller.id)
        else:
            web_users = None

        param = {
            "users": web_users,
            "id": pwg_ids,
            "name": str(name) + " Transfer to Users below",
        }
        return render(request, 'seller/transfer-seller-pwg.html', param)

    return redirect('seller-pwg')


def seller_authorized(request, pk):
    user = User.objects.get(id=pk)
    pwgserver = PWGServers.objects.all()
    pwg = PWG.objects.all()
    param = {
        "name": "Authorize PWG to User " + user.first_name + " " + user.last_name,
        "pwgserver": pwgserver,
        "pwg": pwg,
        "num": num,
        "id": pk,
        "accType": "seller",
        "target": "user",
        "action": "Authorize",
    }
    return render(request, 'tesafe/transfer.html', param)


def seller_authorized_pwg(request):
    if request.method == "POST":
        ids = request.POST['pwg_ids']
        name = ' '
        pwg_ids = []
        for id in ids:
            if id == ",":
                pass
            else:
                pwg = PWG.objects.get(id=id)
                name = " " + pwg.alias + ", " + name
                pwg_ids.append(pwg.id)

        seller = request.user
        user = User.objects.get(email=seller)
        seller = Seller.objects.get(user=user.id)

        if WebUser.objects.filter(associated_with=seller.id).exists():
            web_users = WebUser.objects.filter(associated_with=seller.id)
        else:
            web_users = None

        param = {
            "users": web_users,
            "id": pwg_ids,
            "name": str(name) + " Authorize to Users below",
            "form_action": "authorize_multiple_pwgs",
            "action": "Authorize",
        }
        return render(request, 'seller/seller-authorized-pwg.html', param)

    return render(request, 'seller/seller-pwg.html')


def seller_shared_pwg(request):
    if request.method == "POST":
        ids = request.POST['pwg_ids']
        name = ''
        pwg_ids = []
        for id in ids:
            if id == ",":
                pass
            elif id == " ":
                pass
            else:
                pwg = PWG.objects.get(id=id)
                name = " " + pwg.alias + ", " + name
                pwg_ids.append(pwg.id)

        seller = request.user
        user = User.objects.get(email=seller)
        seller = Seller.objects.get(user=user.id)

        if WebUser.objects.filter(associated_with=seller.id).exists():
            web_users = WebUser.objects.filter(associated_with=seller.id)
        else:
            web_users = None

        param = {
            "users": web_users,
            "id": pwg_ids,
            "name": str(name) + " Share to Users below",
            "form_action": "share_multiple_pwgs",
            "action": "Share",
        }
        return render(request, 'seller/seller-authorized-pwg.html', param)

    return render(request, 'seller/seller-pwg.html')


def seller_shared(request,pk):
    user = User.objects.get(id=pk)
    pwgserver = PWGServers.objects.all()
    pwg = PWG.objects.all()
    param = {
        "name": "Share PWG to User " + user.first_name + " " + user.last_name,
        "username": user.first_name + " " + user.last_name,
        "pwgserver": pwgserver,
        "pwg": pwg,
        "num": num,
        "id": pk,
        "accType": "seller",
        "target": "user",
        "action": "share",
    }
    return render(request, 'tesafe/transfer.html', param)


def seller_deshared_pwg(request):
    if request.method == "POST":
        ids = request.POST['pwg_ids']
        pwg = PWG.objects.get(id=ids)
        name = pwg.alias

        seller = request.user
        user = User.objects.get(email=seller)
        seller = Seller.objects.get(user=user.id)
        web_usrs = []
        if Share.objects.filter(pwg=pwg).exists():
            web_users = Share.objects.filter(pwg=pwg)
            for usr in web_users:
                web_user = WebUser.objects.get(user=usr.share_to.id)
                web_usrs.append(web_user)
        else:
            web_users = None

        param = {
            "users": web_usrs,
            "id": ids,
            "name": name + ", De-share to Users below",
            "form_action": "deshare_multiple_pwgs",
            "action": "De-share",
        }
    return render(request, 'seller/seller-deshared-pwg.html', param)


def tester_home(request):
    pwgs_untested = []
    pwgs_tested_good = []
    pwgs_tested_faulty = []
    user = request.user
    user = User.objects.get(email=user)
    if PWG.objects.filter(transfer_to=user).exists():
        pwg_obj = PWG.objects.filter(transfer_to=user)
        for pwg in pwg_obj:
            if pwg.is_tested:
                if pwg.is_tested_faulty:
                    pwgs_tested_faulty.append(pwg.owned_by)
                if pwg.is_tested_good:
                    pwgs_tested_good.append(pwg.owned_by)
            else:
                pwgs_untested.append(pwg.owned_by)

    else:
        pwg_obj = None
    if pwg_obj:
        for pwg in pwg_obj:
            pwg_server.append(pwg.owned_by)
    param = {
        'pwg_obj': pwg_obj,
        'pwgs_untested': pwgs_untested,
        'pwgs_tested_good': pwgs_tested_good,
        'pwgs_tested_faulty': pwgs_tested_faulty,
    }
    return render(request, "tester/tester-home.html", param)




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

        else:
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
        return render(request, "index.html")


# to find username
def ajax_request(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the history from the database
        pk = request.GET.get("pk", None)
        accType = request.GET.get("accType", None)
        # check for the pk in the database.

        # if accType is Seller and is seeking history of pwg
        if accType == "seller-pwg":
            if PWGHistory.objects.filter(pwg=pk).exists():
                pwg_history = PWGHistory.objects.filter(pwg=pk)

                pwg_history = serializers.serialize('json', pwg_history)

                return HttpResponse(pwg_history, content_type="application/json")
            else:
                return JsonResponse({"history": False}, status=200)
        else:
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
        # fetching list from AJAX request
        pklist = request.GET.getlist("pk[]", None)
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
        elif accType == 'seller-history':
            pwg_name = []
            print(pklist)
            for id in pklist:
                if id == " ":
                    pass
                elif id == ",":
                    pass
                elif id == "[":
                    pass
                elif id == "]":
                    pass
                else:
                    if User.objects.filter(id=id).exists():
                        u = User.objects.get(id=id)
                        pwg_name.append(u.first_name)

            return JsonResponse({"msg": pwg_name}, status=200)

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
                if i == ",":
                    pass
                elif Seller.objects.filter(id=i).exists():
                    seller = Seller.objects.get(id=i)
                    id_user = seller.user_id
                    seller = User.objects.get(id=id_user)
                    seller.delete()

            return redirect('admin-seller')

        elif accType == "tester":
            for i in values:
                if i == ",":
                    pass
                elif Tester.objects.filter(id=i).exists():
                    tester = Tester.objects.get(id=i)
                    id_user = tester.user_id
                    tester = User.objects.get(id=id_user)
                    tester.delete()

            return redirect('admin-tester')
        elif accType == "pwgs":
            for i in values:
                if i == ",":
                    pass
                elif PWGServers.objects.filter(id=i).exists():
                    pwgs = PWGServers.objects.get(id=i)
                    pwgs.delete()

            return redirect('admin-info-server')
        elif accType == "user":
            for i in values:
                if i == ",":
                    pass
                elif WebUser.objects.filter(id=i).exists():
                    tester = WebUser.objects.get(id=i)
                    user_fk = tester.user
                    tester = User.objects.get(id=user_fk.id)
                    tester.delete()

            return redirect('seller-user')

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
                elif accType == "user":
                    pwg_object.location = "U"
                    pwg_object.save()

                transfer = TransferPwg(pwg_owner=pwg_object, pwgs_owner=pwgs_id, user=current_user)
                transfer.save()

        if accType == "seller":
            return redirect('admin-seller')
        elif accType == "tester":
            return redirect('admin-tester')
        elif accType == "user":
            return redirect('seller-user')

    return redirect('admin-seller')


def authorize_pwgs(request):
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
                pwg_object.is_authorized = True
                pwg_object.save()

                web_user = WebUser.objects.get(user=current_user)
                web_user.is_authorized = True
                web_user.save()

                authorize = Authorize(pwgserver=pwgs_id, authorize_to=current_user, pwg=pwg_object)
                authorize.save()

        if accType == "seller":
            return redirect('seller-user')
        elif accType == "tester":
            return redirect('admin-tester')
        elif accType == "user":
            return redirect('seller-user')

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
        system_name = request.POST.get('system_name', None)
        password = request.POST['password']
        accType = request.POST['accType']
        if system_name:
            serial_no = system_name[-4:]

        if User.objects.filter(email=email).exists():
            messages.info(request, "Email already exists, try again!")
            if accType == "pwgs":
                return redirect("admin-info-server")
            elif accType == "seller":
                return redirect("admin-seller")
            elif accType == "tester":
                return redirect("admin-tester")
            elif accType == "user":
                return redirect("seller-user")

        if accType != "pwgs":
            # creating user
            user = User.objects.create_user(username=email, email=email, first_name=fname, last_name=lname,
                                            password=password)
            user.save()
            if accType == "seller":
                sys_name = SystemName(serial_no=serial_no, user=user, system_name=system_name, is_user=False,
                                      is_seller=True, is_tester=False, is_pwgs=False)
                sys_name.save()
            elif accType == "tester":
                sys_name = SystemName(serial_no=serial_no, user=user, system_name=system_name, is_user=False,
                                      is_seller=False, is_tester=True, is_pwgs=False)
                sys_name.save()
            elif accType == "user":
                sys_name = SystemName(serial_no=serial_no, user=user, system_name=system_name, is_user=True,
                                      is_seller=False, is_tester=False, is_pwgs=False)
                sys_name.save()

        # creating seller account
        if accType == "seller":
            seller = Seller(user=user, first_name=fname, last_name=lname, alias=alias, email=email, phone=number, system_name=system_name)
            seller.save()
            messages.info(request, "Successfully Account Created!")
            return redirect("admin-seller")

        # creating tester account
        elif accType == "tester":
            tester = Tester(user=user, first_name=fname, last_name=lname, alias=alias, email=email, phone=number, system_name=system_name)
            tester.save()
            messages.info(request, "Successfully Account Created!")
            return redirect("admin-tester")

        # creating PWGS account
        elif accType == "pwgs":
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()
            pwgs = PWGServers(alias=alias, email=email, password=password, pwg_count=0, user=user, system_name=system_name)
            pwgs.save()
            sys_name = SystemName(serial_no=serial_no, user=user, system_name=system_name, is_user=False,
                                  is_seller=False, is_tester=False, is_pwgs=True)
            sys_name.save()
            messages.info(request, "Successfully Account Created!")
            return redirect("admin-info-server")
        # creating PWGS account
        elif accType == "user":
            if user is not None:
                seller_id = Seller.objects.get(id=seller_id)
                user_count = seller_id.user_count
                seller_id.user_count = int(user_count) + 1
                user_obj = WebUser(user=user, first_name=fname, last_name=lname, email=email, phone=number, alias=alias, associated_with=seller_id, system_name=system_name)
                user_obj.save()
                seller_id.save()
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
                if i == ",":
                    pass
                elif Seller.objects.filter(id=i).exists():
                    seller = Seller.objects.get(id=i)
                    seller.is_freeze = True
                    seller.save()

            return redirect('admin-seller')

        elif accType == "tester":
            for i in values:
                if i == ",":
                    pass
                elif Tester.objects.filter(id=i).exists():
                    tester = Tester.objects.get(id=i)
                    tester.is_freeze = True
                    tester.save()

            return redirect('admin-tester')
        elif accType == "pwg":
            for i in values:
                if i == ",":
                    pass
                elif PWG.objects.filter(id=i).exists():
                    pwg = PWG.objects.get(id=i)
                    pwg.is_freeze = True
                    pwg.save()
            if pk:
                return redirect('pwg-sublist', id=int(pk))
            else:
                return redirect('admin-info-server')

        elif accType == "user":
            for i in values:
                if i == ",":
                    pass
                elif WebUser.objects.filter(id=i).exists():
                    tester = WebUser.objects.get(id=i)
                    tester.is_freeze = True
                    tester.save()

            return redirect('seller-user')
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


def system_name(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        accType = request.GET.get("accType", None)
        nnn = request.GET.get("nnn", None)
        name = None
        if nnn and accType:
            name = unique_name(accType, nnn)
            return JsonResponse({"msg": name}, status=200)
        else:
            return JsonResponse({"msg": False}, status=200)
    else:
        return JsonResponse({}, status=200)


def deauthorize(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        accType = request.GET.get("accType", None)
        pk = request.GET.get("pk", None)

        if User.objects.filter(id=pk).exists():
            user_obj = User.objects.get(id=pk)
            authorize_obj = Authorize.objects.filter(authorize_to=user_obj.id)
            for item in authorize_obj:
                pwg_obj = item.pwg
                pwg_obj.is_authorized = False
                pwg_obj.save()

                item.delete()

            web_user = WebUser.objects.get(user=pk)
            web_user.is_authorized = False
            name = "{} has been successfully de-authorized from User {}".format(authorize_obj[0].pwg, web_user.first_name)
            web_user.save()
            return JsonResponse({"msg": name}, status=200)
        else:
            return JsonResponse({"msg": False}, status=200)
    else:
        return JsonResponse({}, status=200)


def share_pwgs(request):
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
                pwg_object.is_shared = True
                pwg_object.save()

                user_obj = WebUser.objects.get(user=pk)
                user_obj.is_shared = True
                user_obj.save()

                share_obj = Share(pwg=pwg_object, share_to=current_user, pwgserver=pwgs_id)
                share_obj.save()

        if accType == "seller":
            return redirect('seller-user')
        elif accType == "tester":
            return redirect('admin-tester')
        elif accType == "user":
            return redirect('seller-user')

    return redirect('/')


def deshare(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        accType = request.GET.get("accType", None)
        pk = request.GET.get("pk", None)

        if User.objects.filter(id=pk).exists():
            user_obj = User.objects.get(id=pk)
            share_obj = Share.objects.filter(share_to=pk)
            for item in share_obj:
                pwg_obj = item.pwg
                pwg = PWG.objects.get(id=pwg_obj.id)
                pwg.is_shared = False
                pwg.save()

                item.delete()

            web_user = WebUser.objects.get(user=pk)
            web_user.is_shared = False
            name = "{} has been successfully de-shared from User {}".format(share_obj[0].pwg, web_user.first_name)
            web_user.save()
            return JsonResponse({"msg": name}, status=200)
        else:
            return JsonResponse({"msg": False}, status=200)
    else:
        return JsonResponse({}, status=200)


def authorize_multiple_pwgs(request):
    if request.method == "POST":
        authorize_values = request.POST['authorize_values']
        pwg_values = request.POST['pwg_values']

        for pwg_id in pwg_values:
            print(pwg_id)
            if pwg_id == ",":
                pass
            elif pwg_id == "[":
                pass
            elif pwg_id == "]":
                pass
            elif pwg_id == " ":
                pass
            else:
                pwg_obj = PWG.objects.get(id=pwg_id)
                pwg_obj.is_authorized = True
                pwgs = pwg_obj.owned_by
                pwg_obj.save()
                for user_id in authorize_values:
                    if user_id == ",":
                        pass
                    elif user_id == " ":
                        pass
                    else:
                        user_obj = WebUser.objects.get(id=user_id)
                        user_obj.is_authorized = True
                        u = user_obj.user
                        user_obj.save()

                        if Authorize.objects.filter(authorize_to=u, pwg=pwg_obj).exists():
                            print("not saved")
                        else:
                            authrize_obj = Authorize(pwg=pwg_obj, authorize_to=u, pwgserver=pwgs)
                            authrize_obj.save()

                        pwg_his = PWGHistory(object=u, pwg=pwg_obj, action="A")
                        pwg_his.save()

        return redirect("seller-pwg")

    else:
        return render(request, "seller/seller-pwg.html")


def share_multiple_pwgs(request):
    if request.method == "POST":
        authorize_values = request.POST['authorize_values']
        pwg_values = request.POST['pwg_values']
        for pwg_id in pwg_values:
            if pwg_id == ",":
                pass
            elif pwg_id == "[":
                pass
            elif pwg_id == "]":
                pass
            elif pwg_id == " ":
                pass
            else:
                pwg_obj = PWG.objects.get(id=pwg_id)
                pwg_obj.is_shared = True
                pwgs = pwg_obj.owned_by
                pwg_obj.save()
                for user_id in authorize_values:
                    if user_id == ",":
                        pass
                    elif user_id == " ":
                        pass
                    else:
                        user_obj = WebUser.objects.get(id=user_id)
                        user_obj.is_shared = True
                        u = user_obj.user
                        user_obj.save()

                        if Share.objects.filter(share_to=u, pwg=pwg_obj).exists():
                            print("not saved")
                        else:
                            share_obj = Share(pwg=pwg_obj, share_to=u, pwgserver=pwgs)
                            share_obj.save()

                        pwg_his = PWGHistory(object=u, pwg=pwg_obj, action="S")
                        pwg_his.save()

        return redirect("seller-pwg")

    else:
        return render(request, "seller/seller-pwg.html")


def deshare_multiple_pwgs(request):
    if request.method == "POST":
        authorize_values = request.POST['share_values']
        pwg_values = request.POST['pwg_values']
        for pwg_id in pwg_values:
            if pwg_id == ",":
                pass
            elif pwg_id == "[":
                pass
            elif pwg_id == "]":
                pass
            else:
                pwg_obj = PWG.objects.get(id=pwg_id)
                pwg_obj.is_shared = False
                pwgs = pwg_obj.owned_by
                pwg_obj.save()
                for user_id in authorize_values:
                    if user_id == ",":
                        pass
                    else:
                        user_obj = WebUser.objects.get(id=user_id)
                        user_obj.is_shared = False
                        u = user_obj.user
                        user_obj.save()

                        # saving history
                        # pwg_his = PWGHistory(object=u, pwg=pwg_obj, action="De-shared")

                        if Share.objects.filter(share_to=u, pwg=pwg_obj).exists():
                            share_obj = Share.objects.filter(share_to=u, pwg=pwg_obj)
                            share_obj.delete()

        return redirect("seller-pwg")
    else:
        return render(request, "seller/seller-pwg.html")


def delete_temp(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the history from the database
        pk = request.GET.get("pk", None)
        accType = request.GET.get("accType", None)
        u = request.user

        if accType == "user":
            # check for the pk in the database.
            if WebUser.objects.filter(id=pk).exists():
                my_object = WebUser.objects.get(id=pk)
                my_object.associated_with = None
                name = my_object.first_name
                name = "{} has been successfully deleted from your list".format(name)
                my_object.save()
                return JsonResponse({"msg": name}, status=200)
            else:
                # if name not found, then return msg
                return JsonResponse({"msg": False}, status=200)

        elif accType == "pwg":
            # check for the pk in the database.
            if PWG.objects.filter(id=pk).exists():
                my_object = PWG.objects.get(id=pk)
                my_object.transfer_to = None
                my_object.location = "A"
                name = my_object.alias
                # s = name + " deleted"
                # s = PWGHistory(object=u, pwg=my_object, action=s)
                # s.save()

                name = "{} has been successfully deleted from your list".format(name)
                my_object.save()

                return JsonResponse({"msg": name}, status=200)
            else:
                # if name not found, then return msg
                return JsonResponse({"msg": False}, status=200)

    return JsonResponse({}, status=400)


def return_pwg(request):
    if request.method == "POST":
        ids = request.POST['pwg_ids']
        acctype = request.POST['accType']

        user = request.user
        user = User.objects.get(email=user)
        # fetching superuser's object
        u = User.objects.get(id=1)

        if acctype == "seller":
            for id in ids:
                if id == ",":
                    pass
                elif id == " ":
                    pass
                else:
                    if PWG.objects.filter(id=id).exists():
                        pwg_obj = PWG.objects.get(id=id)
                        pwg_obj.transfer_to = u
                        pwg_obj.sold_from = u
                        pwg_obj.location = "A"
                        pwg_obj.save()

                        if TransferPwg.objects.filter(user=user).exists():
                            trans_pwg = TransferPwg.objects.get(user=user)
                            trans_pwg.delete()

                    else:
                        messages.info(request, "PWG Object not found!")
                        return redirect("seller-pwg")

                    pwg_his = PWGHistory(object=user, pwg=pwg_obj, action="RAD")
                    pwg_his.save()
            return redirect("seller-pwg")

    messages.error(request, 'Something went wrong')
    return redirect("/")


def transfer_pwg_multiple_users(request):
    if request.method == "POST":
        transfer_values = request.POST['transfer_values']
        pwg_values = request.POST['pwg_values']
        for pwg_id in pwg_values:
            if pwg_id == ",":
                pass
            elif pwg_id == "[":
                pass
            elif pwg_id == "]":
                pass
            elif pwg_id == " ":
                pass
            else:
                pwg_obj = PWG.objects.get(id=pwg_id)

                for user_id in transfer_values:
                    if user_id == ",":
                        pass
                    elif user_id == " ":
                        pass
                    else:
                        user_obj = WebUser.objects.get(id=user_id)
                        u = user_obj.user

                        pwg_obj.sold_from = u
                        pwg_obj.is_authorized = False
                        pwg_obj.is_freeze = False
                        pwg_obj.is_shared = False
                        pwg_obj.save()

                        p = PWGHistory(object=u, pwg=pwg_obj, action="T")
                        p.save()

        return redirect("seller-pwg")

    else:
        messages.info(request, "something went wrong try again!")
        return redirect("/")


