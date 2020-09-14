from django.shortcuts import render, redirect
from .models import WebAdmin, Seller, Tester, WebUser, PWGServers, PWG, WebAdminLoginHistory, PasswordHistory
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import JsonResponse


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

                    seller = Seller(user=user, first_name=fname, last_name=lname, email=email, phone=phone)
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

                    tester = Tester(user=user, first_name=fname, last_name=lname, email=email, phone=phone)
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

                    webUser = WebUser(user=user, first_name=fname, last_name=lname, email=email, phone=phone)
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
    return render(request, 'tesafe/admin-seller.html', {'num': [11,23,33,42,35,67,78,49,10]})


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
    return render(request, 'seller/seller-home.html', {'num': [11,23,33,42,35,67,78,49,10]})


def seller_user(request):
    return render(request, 'seller/seller-user.html', {'num': [11,23,33,42,35,67,78,49,10]})


def seller_pwg(request):
    return render(request, 'seller/seller-pwg.html', {'num': [11,23,33,42,35,67,78,49,10]})


def transfer(request):
    return render(request, 'tesafe/transfer.html', {'num': [11,23,33,42,35,67,78,49,10]})


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