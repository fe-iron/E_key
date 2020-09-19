from django.shortcuts import render, redirect
from .models import WebAdmin, Seller, Tester, WebUser, PWGServers, PWG, WebAdminLoginHistory, PasswordHistory, TransferPwgs, TransferPwg
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


def index(request):
    if request.method == 'POST':
        accType = request.POST['accType']
        password = request.POST['password']
        uname = request.POST['uname']
        print(request)

        user = auth.authenticate(username=uname, password=password)

        if user is not None:
            auth.login(request, user)
            # saving history
            ip = get_ip(request)
            device_name = request.META.get("COMPUTERNAME")
            history = WebAdminLoginHistory(user=user, login_IP=ip, device_name=device_name)
            history.save()

            if accType == 'admin':
                return admin_home(request)
            elif accType == 'seller':
                return seller_home(request)
            elif accType == 'tester':
                return render(request, 'tester/tester-home.html', {'num': [11, 23, 33, 42, 35, 67, 78, 49, 10]})
            elif accType == 'user':
                return render(request, 'user/user-home.html', {'num': [11, 23, 33, 42, 35, 67, 78, 49, 10]})


        else:
            messages.info(request, 'Invalid user id and password')
            return redirect('/')

    else:
        print(request)
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
        file = request.POST['file']
        device = request.META.get("COMPUTERNAME")

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

                # if it is admin
                if accType == 'admin':
                    user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email, password=password1)
                    user.save()

                    # creating password history
                    passHistory = PasswordHistory(user=user, device_name=device,last_pass=password1)
                    passHistory.save()

                    webAdmin = WebAdmin(user=user, first_name=fname, last_name=lname, email=email, phone=phone)
                    webAdmin.save()

                    return render(request, 'tesafe/admin-home.html')

                # if it is seller
                elif accType == 'seller':
                    user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email, password=password1)
                    user.save()

                    # creating password history
                    passHistory = PasswordHistory(user=user, device_name=request.META.get("COMPUTERNAME"),
                                                  last_pass=password1)
                    passHistory.save()

                    seller = Seller(user=user, first_name=fname, last_name=lname, email=email, phone=phone, profile_pic=file)
                    seller.save()

                    return render(request, 'seller/seller-home.html')

                # if it is tester
                elif accType == 'tester':

                    user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email,
                                                    password=password1)
                    user.save()

                    # creating password history
                    passHistory = PasswordHistory(user=user, device_name=request.META.get("COMPUTERNAME"),
                                                  last_pass=password1)
                    passHistory.save()

                    tester = Tester(user=user, first_name=fname, last_name=lname, email=email, phone=phone, profile_pic=file)
                    tester.save()

                    return render(request, 'tester/tester-home.html')

                # if it is user
                elif accType == 'user':
                    user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email,
                                                    password=password1)
                    user.save()

                    # creating password history
                    passHistory = PasswordHistory(user=user, device_name=request.META.get("COMPUTERNAME"),
                                                  last_pass=password1)
                    passHistory.save()

                    webUser = WebUser(user=user, first_name=fname, last_name=lname, email=email, phone=phone, profile_pic=file)
                    webUser.save()

                    return render(request, 'tester/tester-home.html')
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
        'num': [11, 23, 33, 42, 35, 67, 78, 49, 10],
        'seller_online': queryset_seller.count(),
        'seller_offline': seller_count - queryset_seller.count(),
        'tester_online': queryset_tester.count(),
        'tester_offline': tester_count - queryset_tester.count(),
        'web_user_online': queryset_web_user.count(),
        'web_user_offline': web_user_count - queryset_web_user.count(),
        'PWGs_offline': PWGS_count - queryset_PWGs.count(),
        'PWGs_online': queryset_PWGs.count(),
        'history': WebAdminLoginHistory.objects.filter(user=request.user),
        'history_count': history_count,
        'password_history': PasswordHistory.objects.filter(user=request.user)
    }
    return render(request, 'tesafe/admin-home.html', params)


def admin_seller(request):
    seller = Seller.objects.all()
    history = WebAdminLoginHistory.objects.all()
    param = {
        'seller': seller,
        'history': history
    }
    return render(request, 'tesafe/admin-seller.html', param)


def admin_tester(request):
    return render(request, 'tesafe/admin-tester.html', {'num': [11,23,33,42,35,67,78,49,10]})


def admin_info_server(request):
    return render(request, 'tesafe/admin-info-server.html', {'num': [11, 23, 33, 42, 35, 67, 78, 49, 10]})


def register_next(request):
    if request.method == 'POST':
        accType = request.POST['accType']
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['uname']
        email = request.POST['email']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if accType == 'admin':
            if password1 == password2:
                user = User.objects.create_user(username=uname, first_name=fname, last_name=lname, email=email,
                                                password=password1, is_webAdmin=True)
                user.save()

                webAdmin = WebAdmin(name=fname, phone=phone, email=email)
                webAdmin.save()
                msg = messages.info("Account successfully created!")
                return render(request, 'tesafe/admin-page.html', {'msg': msg})

            else:
                msg = messages.error(request, "Password do not match! try again")
                return render(request, 'tesafe/admin-page.html', {'msg': msg})

    return render(request, 'tesafe/admin-seller.html', {})


def seller_home(request):
    seller = Seller.objects.all()
    param = {
        'seller': seller
    }
    return render(request, 'seller/seller-home.html', param)


def seller_user(request):
    return render(request, 'seller/seller-user.html', {'num': [11,23,33,42,35,67,78,49,10]})


def seller_pwg(request):
    return render(request, 'seller/seller-pwg.html', {'num': [11,23,33,42,35,67,78,49,10]})


def transfer(request, id):
    user = User.objects.get(id=id)
    pwgserver = PWGServers.objects.all()
    pwg = PWG.objects.all()
    param = {
        "name": user.first_name + " " + user.last_name,
        "pwgserver": pwgserver,
        "pwg": pwg,
        "num": num,
        "id": id
    }
    return render(request, 'tesafe/transfer.html', param)


def tester_getback(request):
    return render(request, 'tesafe/tester-getback.html', {'num': [11,23,33,42,35,67,78,49,10]})


def tester_tested_pwg_list(request):
    return render(request, 'tesafe/tester-tested-pwg-list.html', {'num': [11,23,33,42,35,67,78,49,10]})


def pwg_sublist(request):
    return render(request, 'tesafe/pwg-sublist.html', {'num': [11,23,33,42,35,67,78,49,10]})


def pwg_getback(request):
    return render(request, 'tesafe/pwg-getback.html', {'num': [11,23,33,42,35,67,78,49,10]})


def pwg_getback_sublist(request):
    return render(request, 'tesafe/pwg-getback-sublist.html', {'num': [11,23,33,42,35,67,78,49,10]})


def tester_pwg_sublist(request):
    return render(request, 'tesafe/tester-pwg-sublist.html', {'num': [11, 23, 33, 42, 35, 67, 78, 49, 10]})


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
        old_email = request.POST['old_email']
        new_email = request.POST['new_email']
        new_conf_email = request.POST['new_conf_email']
        if new_conf_email == new_email:
            # creating password history
            passHistory = PasswordHistory(user=request.user, device_name=request.META.get("COMPUTERNAME"), last_pass=new_email)
            passHistory.save()

            user = User.objects.get(username=old_email)
            user.set_password(new_email)
            user.save()
            messages.info(request, "Successfully changed your password")
            return redirect("/")
        else:
            messages.info("Email doesn't match!")
            return render(request, "tesafe/admin-home.html#change-passward")

    else:
        return render(request, "index.html")


def ajax_request(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the history from the database
        pk = request.GET.get("pk", None)
        # check for the pk in the database.
        if WebAdminLoginHistory.objects.filter(user_id=pk).exists():
            # if history found return history
            history = WebAdminLoginHistory.objects.filter(user_id=pk)
            name = WebAdminLoginHistory.objects.get(user_id=pk)
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
        # check for the pk in the database.
        if User.objects.filter(pk=pk).exists():
            name = User.objects.get(pk=pk)
            name1 = name.first_name
            return JsonResponse({"name": name1}, status=200)
        else:
            # if name not found, then return true
            return JsonResponse({"name": False}, status=200)

    return JsonResponse({}, status=400)


def delete(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the history from the database
        pk = request.GET.get("pk", None)
        user = request.GET.get("user", None)
        # if user == "seller":
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

    return redirect('admin-seller')


def transfer_pwgs(request):
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
        pwg = set(pwg)
        pwg = list(pwg)

        if len(pwg_server) != 0:
            for i in pwg_server:
                pwgs = PWGServers.objects.get(id=i)
                name = pwgs.name
                # print(name)
                transfer = TransferPwgs(pwgs_name=name, pwgs_owner=pwgs, user=current_user)
                transfer.save()

        if len(pwg) != 0:
            for i in pwg:
                pwg_object = PWG.objects.get(id=i)
                name = pwg_object.name
                transfer = TransferPwg(pwg_name=name, pwg_owner=pwg_object, user=current_user)
                transfer.save()

        return redirect('admin-seller')
    return redirect('admin-seller')


def add_new(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        alias = request.POST['alias']
        email = request.POST['email']
        number = request.POST['number']
        password = request.POST['password']
        accType = request.POST['accType']

        # creating user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()

        # creating seller account
        if accType == "seller":
            seller = Seller(user=user, first_name=fname, last_name=lname, alias=alias, email=email, phone=number)
            seller.save()
            return redirect("admin-seller")

        # creating tester account
        elif accType == "tester":
            tester = Tester(user=user, first_name=fname, last_name=lname, alias=alias, email=email, phone=number)
            tester.save()
            return redirect("admin-tester")

    else:
        return redirect("admin-seller")


def freeze_multiple_user(request):
    # request's method  should be POST
    if request.method == "POST":
        sellers = []
        # fetch the data from the request
        values = request.POST.get("freeze_values", None)
        accType = request.POST.get("accType", None)

        # print(values)
        if accType == "seller":
            for i in values:
                if Seller.objects.filter(id=i).exists():
                    seller = Seller.objects.get(id=i)
                    seller.is_freeze = True
                    seller.save()

            return redirect('admin-seller')

    return redirect('admin-seller')
