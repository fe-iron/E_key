from .models import WebAdmin, Seller, Tester, WebUser, PWGServers, PWG, WebAdminLoginHistory, PasswordHistory, \
    TransferPwgs, TransferPwg, PwgUseRecord, SystemName, Authorize, Share, PWGHistory, TesterPWGHistory, \
    UserToUser, MessageModel, UserLogin
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text
from django.contrib.sessions.models import Session
from django.core.mail import send_mail, EmailMessage
from django.contrib.sessions.models import Session
from django.contrib.auth.models import auth, User
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
from django.contrib import messages
from django.utils import timezone
# password resset email imports
from django.urls import reverse
from .utils import unique_name
from django.db.models import Q
from django.views import View
import threading
import datetime
import json

# global vars
webAdmin = 0
webUser = 0
seller = 0
tester = 0
webUser_email = []


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


# password reset views as class based views
class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, "authentication/reset-password.html")

    def post(self, request):
        email = request.POST['email']

        if not User.objects.filter(email=email).exists():
            messages.error(request, "Email does not exists! try again")
            return render(request, "authentication/reset-password.html")
        else:
            user_obj = User.objects.filter(email=email)
            email_contents = {
                'user': user_obj[0],
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user_obj[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user_obj[0])
            }
            link = reverse('reset-user-password', kwargs={
                'uidb64': email_contents['uid'],
                'token': email_contents['token']
            })
            email_subject = 'Password Reset Instructions'
            reset_url = 'http://'+email_contents['domain'] + link

            email = EmailMessage(
                email_subject,
                'Hii there, Please follow the below link to reset your password\n' + reset_url,
                'noreply@tesafe.com',
                [email]
            )
            # email.send(fail_silently=False)
            EmailThread(email).start()

            messages.success(request, "We have sent an email to reset the password")
            return render(request, "authentication/reset-password.html")


class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        param = {
            'uidb64': uidb64,
            'token': token
        }
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk = user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, "Link is already used, please generate a new one")
                return render(request, "authentication/reset-password.html")
        except:
            pass
        return render(request, "authentication/set-new-password.html", param)

    def post(self, request, uidb64, token):
        param = {
            'uidb64': uidb64,
            'token': token
        }
        pass1 = request.POST['password']
        pass2 = request.POST['password1']
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk = user_id)
            user.set_password(pass1)
            user.save()

            if request.user_agent.device.family == "Other":
                device_name = request.user_agent.os.family
                device_name = device_name + " " + str(request.user_agent.os.version).replace(",", "")
            else:
                device_name = request.user_agent.device.family

            pass_his = PasswordHistory(user=user, device_name=device_name, last_pass=pass1)
            pass_his.save()

            messages.success(request, "Password reset successful, now you can login with the new password")
            return redirect("/")
        except Exception as e:
            messages.info(request, "Something went wrong, try again")
            return redirect("/")


def custom_chat(request):
    if request.method == "POST":
        selected_user = request.POST.get('email_user', None)
        if User.objects.filter(Q(email=selected_user) | Q(username=selected_user)).exists():
            usr = User.objects.get(Q(email=selected_user) | Q(username=selected_user))
            usr = usr.first_name
            param = {
                'selected_user': selected_user,
                'name': usr,
            }
            return render(request, 'core/single-chat.html', param)
    return redirect("/")


def broadcast_admin(request):
    user = User.objects.all()
    count = 0
    new_values = ''
    temp_list = []
    for usr in user:
        count += 1
        if count >= 15:
            pass
        else:
            if usr.first_name == '':
                pass
            else:
                new_values += usr.first_name
                new_values += ', '
        temp_list.append(usr.email)

    if count > 15:
        new_values = new_values[:-2]
        new_values += ' + ' + str(count-15) + " others"
    else:
        new_values = new_values[:-2]
        removal = ","
        reverse_removal = removal[::-1]

        replacement = ", and "
        reverse_replacement = replacement[::-1]
        new_values = new_values[::-1].replace(reverse_removal, reverse_replacement, 1)[::-1]

    param = {
        "name": new_values,
        "selected_user": json.dumps(temp_list),
        "action": "Broadcasting",
    }
    return render(request, "core/chat.html", param)


def broadcast(request):
    if request.is_ajax and request.method == "GET":
        recipient = request.GET.getlist('recipient[]', None)
        body = request.GET.get('body', None)
        user = request.user
        user = User.objects.get(Q(email=user) | Q(username=user))
        for receiver in recipient:
            if User.objects.filter(email=receiver).exists():
                usr = User.objects.get(email=receiver)
                msg = MessageModel(user=user, recipient=usr, body=body, first_name=user.first_name)
                msg.save()
            else:
                return JsonResponse({"result": False}, status=200)
        msg = MessageModel.objects.filter(user=user)[:1]
        msg = serializers.serialize('json', msg)
        return HttpResponse(msg, content_type="application/json")


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


def login_history(request, user):
    ip = get_ip(request)
    if request.user_agent.device.family == "Other":
        device_name = request.user_agent.os.family
        device_name = device_name + " " + str(request.user_agent.os.version).replace(",", "")
    else:
        device_name = request.user_agent.device.family

    history = WebAdminLoginHistory(user=user, login_IP=ip, device_name=device_name)
    history.save()


#  login
def index(request):
    if request.method == 'POST':
        accType = request.POST['accType']
        password = request.POST['password']
        uname = request.POST['uname']

        if accType == 'admin':
            user = auth.authenticate(username=uname, password=password)

            if user is not None:
                if WebAdmin.objects.filter(user=user).exists():
                    if UserLogin.objects.filter(user=user).exists():
                        messages.info(request, "Admin is already logged in")
                        return redirect("/")

                    auth.login(request, user)
                    login_history(request, user)

                    # set new session_key for user instance
                    session_key = request.session.session_key
                    u_login = UserLogin(user=user, session_key=session_key, acctype='A')
                    u_login.save()

                    global webAdmin
                    webAdmin += 1
                    return redirect("admin-home")
                else:
                    messages.info(request, 'Invalid user id and password for Admin')
                    return redirect('/')
            else:
                messages.info(request, 'Invalid user id and password')
                return redirect('/')

        elif accType == 'seller':
            user = auth.authenticate(username=uname, password=password)

            if user is not None:
                if Seller.objects.filter(email=uname).exists():
                    if UserLogin.objects.filter(user=user).exists():
                        messages.info(request, "Seller is already logged in")
                        return redirect("/")

                    sel = Seller.objects.get(email=uname)
                    if sel.is_freeze:
                        messages.info(request, "Sorry, this account has been freezed")
                        return redirect("/")
                    auth.login(request, user)
                    login_history(request, user)

                    # set new session_key for user instance
                    session_key = request.session.session_key
                    u_login = UserLogin(user=user, session_key=session_key, acctype='S')
                    u_login.save()

                    global seller
                    seller += 1
                    return redirect("seller-home")
                else:
                    messages.info(request, 'Invalid user id and password for Seller')
                    return redirect('/')
            else:
                messages.info(request, 'Invalid user id and password')
                return redirect('/')

        elif accType == 'tester':
            user = auth.authenticate(username=uname, password=password)

            if user is not None:
                if Tester.objects.filter(email=uname).exists():
                    if UserLogin.objects.filter(user=user).exists():
                        messages.info(request, "Tester is already logged in")
                        return redirect("/")

                    tes = Tester.objects.get(email=uname)
                    if tes.is_freeze:
                        messages.info(request, "Sorry, this account has been freezed")
                        return redirect("/")
                    auth.login(request, user)
                    login_history(request, user)

                    # set new session_key for user instance
                    session_key = request.session.session_key
                    u_login = UserLogin(user=user, session_key=session_key, acctype='T')
                    u_login.save()

                    global tester
                    tester += 1
                    return redirect('tester-home')
                else:
                    messages.info(request, 'Invalid user id and password for Tester')
                    return redirect('/')
            else:
                messages.info(request, 'Invalid user id and password')
                return redirect('/')

        elif accType == 'user':
            user = auth.authenticate(username=uname, password=password)

            if user is not None:
                if WebUser.objects.filter(email=uname).exists():
                    if UserLogin.objects.filter(user=user).exists():
                        messages.info(request, "User is already logged in")
                        return redirect("/")

                    wuser = WebUser.objects.get(email=uname)
                    if wuser.is_freeze:
                        messages.info(request, "Sorry, this account has been freezed")
                        return redirect("/")
                    auth.login(request, user)
                    login_history(request, user)

                    # set new session_key for user instance
                    session_key = request.session.session_key
                    u_login = UserLogin(user=user, session_key=session_key, acctype='U')
                    u_login.save()

                    global webUser, webUser_email
                    webUser += 1
                    webUser_email.append(user)
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
        system_name = request.POST.get('system_name', None)
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        file = request.FILES.get('file', None)

        if system_name:
            serial_no = system_name[-4:]

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

                    sys_name = SystemName(serial_no=serial_no, user=user, system_name=system_name, is_user=False,
                                          is_seller=False, is_tester=False, is_pwgs=False, is_admin=True)
                    sys_name.save()
                    return redirect("admin-home")

                # if it is seller
                elif accType == 'seller':
                    user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email, password=password1)
                    user.save()

                    # creating password history
                    passHistory = PasswordHistory(user=user, device_name=device_name, last_pass=password1)
                    passHistory.save()

                    seller = Seller(user=user, first_name=fname, last_name=lname, email=email, phone=phone, profile_pic=file, alias=uname)
                    seller.save()

                    sys_name = SystemName(serial_no=serial_no, user=user, system_name=system_name, is_user=False,
                                          is_seller=True, is_tester=False, is_pwgs=False, is_admin=False)
                    sys_name.save()

                    return redirect('seller-home')

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

                    sys_name = SystemName(serial_no=serial_no, user=user, system_name=system_name, is_user=False,
                                          is_seller=False, is_tester=True, is_pwgs=False, is_admin=False)
                    sys_name.save()

                    return redirect('tester-home')

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

                    sys_name = SystemName(serial_no=serial_no, user=user, system_name=system_name, is_user=True,
                                          is_seller=False, is_tester=False, is_pwgs=False, is_admin=False)
                    sys_name.save()

                    return redirect('user-home')
        else:
            messages.error(request, "Password do not match! try again")
            return redirect('register')

    return render(request, 'tesafe/register.html')


def logout(request):
    u = request.user

    if WebAdmin.objects.filter(email=u).exists():
        global webAdmin
        webAdmin -= 1
    elif WebUser.objects.filter(email=u).exists():
        global webUser, webUser_email
        webUser -= 1
        webUser_email = list(filter((u).__ne__, webUser_email))
    elif Seller.objects.filter(email=u).exists():
        global seller
        seller -= 1
    elif Tester.objects.filter(email=u).exists():
        global tester
        tester -= 1
    auth.logout(request)
    if User.objects.filter(Q(email=u) | Q(username=u)).exists():
        user = User.objects.get(Q(email=u) | Q(username=u))
        if UserLogin.objects.filter(user=user).exists():
            u_login = UserLogin.objects.get(user=user)
            u_login.delete()
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
    u = request.user
    global webUser, seller, tester
    u = User.objects.get(Q(username=u) | Q(email=u))
    u_email = u.email
    if u.is_authenticated and WebAdmin.objects.filter(email=u_email).exists():
        seller_count = Seller.objects.all().count()
        tester_count = Tester.objects.all().count()
        web_user_count = WebUser.objects.all().count()
        PWGS_count = PWGServers.objects.all().count()

        queryset_PWGs = get_current_users(PWGServers)
        history_count = WebAdminLoginHistory.objects.filter(user=request.user).count()
        cond = ['-login_date', '-login_time']
        params = {
            'seller_count': seller_count,
            'tester_count': tester_count,
            'web_user_count': web_user_count,
            'PWGs_count': PWGS_count,
            'seller_online': abs(seller),
            'seller_offline': abs(seller_count - seller),
            'tester_online': tester,
            'tester_offline': abs(tester_count - tester),
            'web_user_online': webUser,
            'web_user_offline': abs(web_user_count - webUser),
            'PWGs_offline': 0,
            'PWGs_online': queryset_PWGs.count(),
            'history': WebAdminLoginHistory.objects.filter(user=request.user).order_by(*cond),
            'history_count': history_count,
            'password_history': PasswordHistory.objects.filter(user=request.user).order_by(*cond)
        }
        return render(request, 'tesafe/admin-home.html', params)
    messages.error(request, "Login first then try again!!")
    return redirect("/")


def admin_seller(request):
    u = request.user
    u = User.objects.get(Q(username=u) | Q(email=u))
    u_email = u.email
    if u.is_authenticated and WebAdmin.objects.filter(email=u_email).exists():
        seller = Seller.objects.all().order_by('alias')
        param = {
            'seller': seller,
        }
        return render(request, 'tesafe/admin-seller.html', param)
    messages.error(request, "Login first then try again!!")
    return redirect("/")


@login_required
def admin_tester(request):
    u = request.user
    u = User.objects.get(Q(username=u) | Q(email=u))
    u_email = u.email
    if u.is_authenticated and WebAdmin.objects.filter(email=u_email).exists():
        tester = Tester.objects.all().order_by('alias')
        param = {
            'tester': tester,
        }

        return render(request, 'tesafe/admin-tester.html', param)
    messages.error(request, "Login first then try again!!")
    return redirect("/")


@login_required
def admin_info_server(request):
    u = request.user
    u = User.objects.get(Q(username=u) | Q(email=u))
    u_email = u.email
    if u.is_authenticated and WebAdmin.objects.filter(email=u_email).exists():
        pwgs = PWGServers.objects.all().order_by('alias')
        pwg = PWG.objects.all().order_by('alias')
        count_pwgs = pwgs.count()
        count_pwg = pwg.count()
        pwgs_active = get_current_users(PWGServers).count()
        pwg_active = get_current_users(PWG).count()
        param = {
            'pwgs': pwgs,
            'pwg': pwg,
            'total_pwgs': count_pwgs,
            'total_pwgs_online': pwgs_active,
            'total_pwgs_offline': 0,
            'total_pwg': count_pwg,
            'total_pwg_online': pwg_active,
            'total_pwg_offline': 0,
        }
        return render(request, 'tesafe/admin-info-server.html', param)
    messages.error(request, "Login first then try again!!")
    return redirect("/")


@login_required
def seller_home(request):
    u = request.user
    u = User.objects.get(Q(username=u) | Q(email=u))
    u_email = u.email
    if u.is_authenticated and Seller.objects.filter(email=u_email).exists():
        count = 0
        user_count = 0
        user_online = 0
        user_offline = 0
        cond = ['-login_date', '-login_time']
        seller_user = request.user
        seller = seller_user.id
        seller = Seller.objects.get(user=seller)
        if PWG.objects.filter(transfer_to=seller_user).exists():
            pwg = PWG.objects.filter(transfer_to=seller_user)
            count = pwg.count()

        history_count = WebAdminLoginHistory.objects.filter(user=request.user).count()
        history = WebAdminLoginHistory.objects.filter(user=request.user).order_by(*cond)
        global webUser_email
        for email in webUser_email:
            if WebUser.objects.filter(email=email).exists():
                wuser = WebUser.objects.get(email=email)
                if seller == wuser.associated_with:
                    user_count += 1
        param = {
            "seller": seller,
            "pwgs": count,
            "pwg_online": get_current_users(PWG).count(),
            "pwg_offline": count - get_current_users(PWG).count(),
            "user_online": user_count,
            "user_offline": seller.user_count - user_count,
            "history_count": history_count,
            "history": history,
            'password_history': PasswordHistory.objects.filter(user=request.user).order_by(*cond),
        }
        return render(request, 'seller/seller-home.html', param)
    messages.error(request, "Login first then try again!!")
    return redirect("/")


@login_required
def seller_user(request):
    u = request.user
    u = User.objects.get(Q(username=u) | Q(email=u))
    u_email = u.email
    if u.is_authenticated and Seller.objects.filter(email=u_email).exists():
        seller = request.user
        user = User.objects.get(email=seller)
        seller = Seller.objects.get(user=user.id)

        if WebUser.objects.filter(associated_with=seller.id).exists():
            web_users = WebUser.objects.filter(associated_with=seller.id).order_by('alias')
        else:
            web_users = None

        param = {
            "users": web_users,
            "id": seller.id,
            "unique_name": unique_name("S", '001'),
        }
        return render(request, 'seller/seller-user.html', param)
    messages.error(request, "Login first then try again!!")
    return redirect("/")


@login_required
def seller_pwg(request):
    u = request.user
    u = User.objects.get(Q(username=u) | Q(email=u))
    u_email = u.email
    if u.is_authenticated and Seller.objects.filter(email=u_email).exists():
        pwgserver = []
        pwgserver1 = []
        user = request.user
        pwg = PWG.objects.filter(Q(transfer_to=user) | Q(sold_from=user)).order_by('alias')
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
            # "num": num,
        }
        return render(request, 'seller/seller-pwg.html', param)
    messages.error(request, "Login first then try again!!")
    return redirect("/")


def transfer(request, id):
    user = User.objects.get(id=id)
    pwgserver = []
    pwg = PWG.objects.filter(location="A")
    for pwg_obj in pwg:
        try:
            pwgserver.index(pwg_obj.owned_by)
        except ValueError as ve:
            pwgserver.append(pwg_obj.owned_by)
    param = {
        "name": "Transfer PWG to Seller "+user.first_name + " " + user.last_name,
        "username": user.first_name + " " + user.last_name,
        "pwgserver": pwgserver,
        "pwg": pwg,
        "num": num,
        "id": id,
        "for_Admin": "admin",
        "accType": "admin",
        "target": "seller",
        "action": "Transfer",
    }
    return render(request, 'tesafe/transfer.html', param)


@login_required
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


@login_required
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


@login_required
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


@login_required
def transfer_seller(request, pk):
    pwg = PWG.objects.all()
    pwgserver = PWGServers.objects.all()

    user = User.objects.get(id=pk)
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
def tester_home(request):
    u = request.user
    u = User.objects.get(Q(username=u) | Q(email=u))
    u_email = u.email
    if u.is_authenticated and Tester.objects.filter(email=u_email).exists():
        pwgs_untested = []
        pwgs_tested_good = []
        pwgs_tested_faulty = []
        user = request.user
        if User.objects.filter(email=user).exists():
            user = User.objects.get(email=user)
            if PWG.objects.filter(transfer_to=user).exists():
                pwg_obj = PWG.objects.filter(transfer_to=user)
                for pwg in pwg_obj:
                    if pwg.is_tested:
                        if pwg.is_tested_faulty:
                            # checking if the server name is already available or not
                            try:
                                a = pwgs_tested_faulty.index(pwg.owned_by)
                            except ValueError as ve:
                                pwgs_tested_faulty.append(pwg.owned_by)

                        if pwg.is_tested_good:
                            # checking if the server name is already available or not
                            try:
                                a = pwgs_tested_good.index(pwg.owned_by)
                            except ValueError as ve:
                                pwgs_tested_good.append(pwg.owned_by)
                    else:
                        try:
                            a = pwgs_untested.index(pwg.owned_by)
                        except ValueError as ve:
                            pwgs_untested.append(pwg.owned_by)

            else:
                pwg_obj = None

            param = {
                'pwg_obj': pwg_obj,
                'pwgs_untested': pwgs_untested,
                'pwgs_tested_good': pwgs_tested_good,
                'pwgs_tested_faulty': pwgs_tested_faulty,
            }
            return render(request, "tester/tester-home.html", param)

        messages.error(request, "User not available, please login first")
        return render(request, "tester/tester-home.html")
    messages.error(request, "please login first, then try again!!")
    return redirect("/")


@login_required
def tester_test(request):
    u = request.user
    u = User.objects.get(Q(username=u) | Q(email=u))
    u_email = u.email
    if u.is_authenticated and Tester.objects.filter(email=u_email).exists():
        user = request.user
        if User.objects.filter(email=user).exists():
            untested_pwg = []
            pwg_untested = PWG.objects.filter(transfer_to=user)
            for pwg in pwg_untested:
                if not pwg.is_tested:
                    untested_pwg.append(pwg)

            param = {
                'pwg_untested': untested_pwg
            }
            return render(request, 'tester/tester-test.html', param)
        else:
            messages.error(request, "user not available, please login first!")
            return render(request, 'tester/tester-test.html')
    messages.error(request, "please login first, then try again!!")
    return redirect("/")


@login_required
def user_user(request):
    u = request.user
    u = User.objects.get(Q(username=u) | Q(email=u))
    u_email = u.email
    if u.is_authenticated and WebUser.objects.filter(email=u_email).exists():
        user_obj = WebUser.objects.get(user=u)
        if UserToUser.objects.filter(main_user=user_obj).exists():
            user_obj = UserToUser.objects.filter(main_user=user_obj).order_by('associated_user')
            param = {
                "user_obj": user_obj
            }
            return render(request, 'user/user-user.html', param)
        messages.info(request, "You don't have any user, add first!")
        return render(request, 'user/user-user.html')
    messages.error(request, "please login first, then try again!!")
    return redirect("/")


@login_required
def user_home(request):
    u = request.user
    u = User.objects.get(Q(username=u) | Q(email=u))
    u_email = u.email
    if u.is_authenticated and WebUser.objects.filter(email=u_email).exists():
        if PWG.objects.filter(sold_from=u).exists():
            pwg_obj = PWG.objects.filter(sold_from=u)
            u_obj = WebUser.objects.get(user=u)
            param = {
                "pwg_obj": pwg_obj,
                "pk": u_obj.id,
            }
            return render(request, 'user/user-home.html', param)
        messages.error(request, "You have no PWG, Buy one first!")
        return render(request, "user/user-home.html")
    messages.error(request, "please login first, then try again!!")
    return redirect("/")


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
                cond = ['-date', '-time']
                pwg_history = PWGHistory.objects.filter(pwg=pk).order_by(*cond)

                pwg_history = serializers.serialize('json', pwg_history)

                return HttpResponse(pwg_history, content_type="application/json")
            else:
                return JsonResponse({"history": False}, status=200)
        else:
            if WebAdminLoginHistory.objects.filter(user_id=pk).exists():
                # if history found return history
                cond = ['-login_date', '-login_time']
                history = WebAdminLoginHistory.objects.filter(user_id=pk).order_by(*cond)
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
        elif accType == 'pwgs':
            if User.objects.filter(id=pk).exists():
                pwgs = User.objects.get(id=pk)
                name = pwgs.first_name
                return JsonResponse({"name": name}, status=200)
            else:
                # if name not found, then return true
                return JsonResponse({"name": False}, status=200)

        elif accType == 'seller-history':
            pwg_name = []
            new_values = []
            temp_list = ''

            for i in pklist:
                if i == ",":
                    new_values.append(int(temp_list))
                    temp_list = ''
                elif i == " ":
                    pass
                elif i == "[":
                    pass
                elif i == "]":
                    pass
                else:
                    temp_list += i
            new_values.append(int(temp_list))
            pklist = new_values
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
        new_values = []
        temp_list = ''

        for i in values:
            if i == ",":
                new_values.append(int(temp_list))
                temp_list = ''
            elif i == " ":
                pass
            else:
                temp_list += i
        new_values.append(int(temp_list))

        if accType == "seller":
            for val in new_values:
                if val == ",":
                    pass
                elif val == " ":
                    pass
                else:
                    if Seller.objects.filter(id=val).exists():
                        seller = Seller.objects.get(id=val)
                        id_user = seller.user_id
                        tester = User.objects.get(id=id_user)
                        name = tester.first_name
                        tester.delete()
                        messages.info(request, "{} Seller successfully deleted!".format(name))
                    else:
                        messages.info(request, "Seller is not deleted!")
                        return redirect("admin-seller")
            return redirect('admin-seller')

        elif accType == "tester":
            for i in new_values:
                if i == ",":
                    pass
                elif Tester.objects.filter(id=i).exists():
                    tester = Tester.objects.get(id=i)
                    id_user = tester.user_id
                    tester = User.objects.get(id=id_user)
                    name = tester.first_name
                    tester.delete()
                    messages.info(request, "{} Tester successfully deleted!".format(name))
                else:
                    messages.info(request, "Tester is not deleted!")
                    return redirect("admin-tester")
            return redirect('admin-tester')
        elif accType == "pwgs":
            for i in new_values:
                if i == ",":
                    pass
                elif PWGServers.objects.filter(id=i).exists():
                    pwgs = PWGServers.objects.get(id=i)
                    name = pwgs.alias
                    if not name:
                        name = pwgs.system_name
                    pwgs.delete()
                    messages.info(request, "{} PWG Server successfully deleted!".format(name))
                else:
                    messages.info(request, "PWG Server is not deleted!")
                    return redirect("admin-info-server")

            return redirect('admin-info-server')
        elif accType == "user":
            for i in new_values:
                if i == ",":
                    pass
                elif WebUser.objects.filter(id=i).exists():
                    tester = WebUser.objects.get(id=i)
                    user_fk = tester.user
                    tester = User.objects.get(id=user_fk.id)
                    name = tester.first_name
                    tester.delete()
                    messages.info(request, "{} PWG Server successfully deleted!".format(name))
                else:
                    messages.info(request, "User is not deleted!")
                    return redirect("seller-user")
            return redirect('seller-user')

    messages.info(request, "Something went wrong, try again!")
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

        if accType != "admin-info-server":
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

                if accType == "seller":
                    if pwg_object.is_authorized or pwg_object.is_freeze or pwg_object.is_shared:
                        messages.info(request,
                                      " {} PWG is not transferred because either it is Authorized or Shared or Freezed".format(
                                          pwg_object.alias))
                        return redirect('admin-seller')
                    pwg_object.location = "S"
                    pwg_object.transfer_to = current_user
                    pwg_object.save()

                elif accType == "tester":
                    if pwg_object.is_authorized or pwg_object.is_freeze or pwg_object.is_shared:
                        messages.info(request,
                                      " {} PWG is not transferred because either it is Authorized or Shared or Freezed".format(
                                          pwg_object.alias))
                        return redirect('admin-tester')
                    pwg_object.location = "T"
                    pwg_object.transfer_to = current_user
                    pwg_object.save()
                elif accType == "user":
                    pwg_object.sold_from = current_user
                    pwg_object.user_location = "T"
                    if pwg_object.is_authorized or pwg_object.is_freeze or pwg_object.is_shared:
                        messages.info(request, " {} PWG is not transferred because either it is Authorized or Shared or Freezed".format(pwg_object.alias))
                        return redirect('seller-user')

                    pwg_object.save()

                elif accType == "admin-info-server":
                    if Seller.objects.filter(id=pk).exists():
                        if pwg_object.is_authorized or pwg_object.is_freeze or pwg_object.is_shared:
                            messages.info(request,
                                          " {} PWG is not transferred because either it is Authorized or Shared or Freezed".format(
                                              pwg_object.alias))
                            return redirect('admin-info-server')
                        seller_obj = Seller.objects.get(id=pk)
                        my_id = seller_obj.user.id
                        seller_obj = User.objects.get(id=my_id)
                        pwg_object.transfer_to = seller_obj
                        pwg_object.location = "S"
                        pwg_object.save()

                        current_user = seller_obj
                    else:
                        messages.error(request, "something went wrong, try again!")
                        return redirect(accType)

                if accType != "user":
                    # creating entry in PWG Transfer table
                    transfer = TransferPwg(pwg_owner=pwg_object, pwgs_owner=pwgs_id, user=current_user)
                    transfer.save()
                    # creating entry in PWG history table
                    if PWGHistory.objects.filter(object=current_user, pwg=pwg_object, action="T").exists():
                        pass
                    else:
                        pwg_his = PWGHistory(object=current_user, pwg=pwg_object, action="T")
                        pwg_his.save()
                else:
                    # creating entry in PWG history table
                    if PWGHistory.objects.filter(object=current_user, pwg=pwg_object, action="T").exists():
                        pass
                    else:
                        pwg_his = PWGHistory(object=current_user, pwg=pwg_object, action="T")
                        pwg_his.save()
                tester_his = TesterPWGHistory(pwg_name=pwg_object, got_on=datetime.datetime.now())
                tester_his.save()

        if accType == "seller":
            return redirect('admin-seller')
        elif accType == "tester":
            return redirect('admin-tester')
        elif accType == "user":
            return redirect('seller-user')
        elif accType == "admin-info-server":
            return redirect('admin-info-server')

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


# return pwg to admin
def getback_pwgs(request):
    # request's method  should be POST
    if request.method == "POST":
        pwg = []
        pwg_server = []
        flag = False
        # fetch the data from the database

        values = request.POST.get("values", None)
        pk = request.POST.get("user_pk", None)
        accType = request.POST.get("accType", None)

        if pk:
            current_user = User.objects.get(pk=pk)
        # separating pk of PWG Server and PWG
        # print("values ",values)
        for i in range(len(values)):
            if values[i] == 's':
                pwg_server.append(values[i+1])
                flag = True
            elif values[i] == ',':
                pass
            elif values[i] == ' ':
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
                u = request.user
                u = User.objects.get(username='elahi')
                temp_pwg = PWG.objects.get(id=i)
                temp_pwg.location = "A"
                temp_pwg.transfer_to = u
                temp_pwg.save()

                trans_pwg = TransferPwg.objects.get(pwg_owner=i)
                trans_pwg.delete()

                if PWGHistory.objects.filter(object=u, pwg=temp_pwg, action="RAD").exists():
                    pass
                else:
                    pwg_his = PWGHistory(object=u, pwg=temp_pwg, action="RAD")
                    pwg_his.save()

        if accType == "tester-home":
            return redirect('tester-home')
        elif accType == "admin-info-server":
            return redirect("admin-info-server")
        else:
            return redirect('admin-tester')

    return redirect('admin-tester')


def add_new(request):
    if request.method == 'POST':
        fname = request.POST.get('fname', None)
        lname = request.POST.get('lname', None)
        name = str(request.POST.get('name', None))
        alias = request.POST.get('alias', None)
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
            elif accType == "admin":
                return redirect("assist_admin")

        if accType != "pwgs":
            # creating user
            user = User.objects.create_user(username=email, email=email, first_name=fname, last_name=lname,
                                            password=password)
            user.save()
            if accType == "seller":
                sys_name = SystemName(serial_no=serial_no, user=user, system_name=system_name, is_user=False,
                                      is_seller=True, is_tester=False, is_pwgs=False, is_admin=False)
                sys_name.save()
            elif accType == "tester":
                sys_name = SystemName(serial_no=serial_no, user=user, system_name=system_name, is_user=False,
                                      is_seller=False, is_tester=True, is_pwgs=False, is_admin=False)
                sys_name.save()
            elif accType == "user":
                sys_name = SystemName(serial_no=serial_no, user=user, system_name=system_name, is_user=True,
                                      is_seller=False, is_tester=False, is_pwgs=False, is_admin=False)
                sys_name.save()
            elif accType == "admin":
                sys_name = SystemName(serial_no=serial_no, user=user, system_name=system_name, is_user=False,
                                      is_seller=False, is_tester=False, is_pwgs=False, is_admin=True)
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
            if alias != "":
                user = User.objects.create_user(username=email, email=email, password=password, first_name=alias)
            else:
                user = User.objects.create_user(username=email, email=email, password=password, first_name=system_name)
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

        elif accType == "admin":
            if user is not None:
                user_obj = WebAdmin(user=user, first_name=fname, last_name=lname, email=email, phone=number, system_name=system_name, alias=alias)
                user_obj.save()

                messages.info(request, "Successfully Account Created!")
                return redirect("admin-home")
            else:
                messages.info(request, "Something went wrong, try again")
                return redirect("admin-home")
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

        temp_list = ''
        new_values = []
        for i in values:
            if i == ",":
                new_values.append(int(temp_list))
                temp_list = ''
            elif i == " ":
                pass
            else:
                temp_list += i
        new_values.append(int(temp_list))
        values = new_values
        # print(values)
        if accType == "seller":
            for i in values:
                if i == ",":
                    pass
                else:
                    if Seller.objects.filter(id=i).exists():
                        seller = Seller.objects.get(id=i)
                        seller.is_freeze = True
                        seller.save()
                    else:
                        messages.error(request, "Some of the Seller(s) was not freezed!")
                        return redirect("admin-seller")
            return redirect('admin-seller')

        elif accType == "tester":
            for i in values:
                if i == ",":
                    pass
                else:
                    if Tester.objects.filter(id=i).exists():
                        tester = Tester.objects.get(id=i)
                        tester.is_freeze = True
                        tester.save()
                    else:
                        messages.error(request, "Some of the Tester(s) was not freezed!")
                        return redirect('admin-tester')
            return redirect('admin-tester')

        elif accType == "pwg":
            for i in values:
                if i == ",":
                    pass
                else:
                    if PWG.objects.filter(id=i).exists():
                        pwg = PWG.objects.get(id=i)
                        pwg.is_freeze = True
                        pwg.save()
                    else:
                        messages.error(request, "Some of the PWG(s) was not freezed!")
                        if pk:
                            return redirect('pwg-sublist', id=int(pk))
                        else:
                            return redirect('admin-info-server')

        elif accType == "user":
            for i in values:
                if i == ",":
                    pass
                else:
                    if WebUser.objects.filter(id=i).exists():
                        tester = WebUser.objects.get(id=i)
                        tester.is_freeze = True
                        tester.save()
                    else:
                        messages.error(request, "Some of the User(s) was not freezed!")
                        return redirect('seller-user')
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
                messages.error(request, "Something went wrong! try again")
                return redirect("admin-info-server")

        elif accType == "pwg":
            if PWG.objects.filter(id=alias_id).exists():
                pwgs = PWG.objects.get(id=alias_id)
                pwgs.alias = alias
                pwgs.save()
                return redirect("user-home")
            else:
                messages.error(request, "Something went wrong! try again")
                return redirect("user-home")

        elif accType == "seller":
            if alias_conf == alias:
                if User.objects.filter(id=alias_id).exists():
                    user_obj = User.objects.get(id=alias_id)
                    if WebUser.objects.filter(user=user_obj.id).exists():
                        user_obj = WebUser.objects.get(user=user_obj.id)
                        user_obj.alias = alias
                        user_obj.save()
                        return redirect("seller-home")
                    else:
                        messages.error(request, "Something went wrong! try again")
                        return redirect("seller-home")
                else:
                    messages.error(request, "Something went wrong! try again")
                    return redirect("seller-home")
            else:
                messages.error(request, "Alias name does not match! try again")
                return redirect("seller-home")

        elif accType == "user-user":
            if WebUser.objects.filter(id=alias_id).exists():
                user_obj = WebUser.objects.get(id=alias_id)
                user_obj.alias = alias
                user_obj.save()
                return redirect("user-user")
            else:
                messages.error(request, "Something went wrong! try again")
                return redirect("user-user")
    else:
        messages.info(request, "Something went wrong! try again")
        return redirect("/")


def getpassword(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the history from the database
        pk = request.GET.get("pk", None)
        if PasswordHistory.objects.filter(user=pk).exists():
            cond = ['-login_date', '-login_time']
            history = PasswordHistory.objects.filter(user=pk).order_by(*cond)
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
        accType = request.GET.get("accType", None)
        if accType == "pwg":
            if PwgUseRecord.objects.filter(pwg=pk).exists():
                use_record = PwgUseRecord.objects.filter(pwg=pk)
                use_record_json = serializers.serialize('json', use_record)

                return HttpResponse(use_record_json, content_type='application/json')
            else:
                return JsonResponse({'history': False}, status=200)

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
        accType = request.POST.get("accType", None)

        new_values = []
        temp_list = ''

        for i in tester_ids:
            if i == ",":
                new_values.append(int(temp_list))
                temp_list = ''
            elif i == " ":
                pass
            else:
                temp_list += i
        new_values.append(int(temp_list))
        tester_ids = new_values
        new_values = []
        temp_list = ''

        for i in pk:
            if i == ",":
                new_values.append(int(temp_list))
                temp_list = ''
            elif i == " ":
                pass
            else:
                temp_list += i
        new_values.append(int(temp_list))
        pk = new_values

        if accType == "admin-tester":
            for i in tester_ids:
                if i == ",":
                    pass
                else:
                    pwg = PWG.objects.get(id=pk[0])
                    pwgs = pwg.owned_by
                    tester = Tester.objects.get(id=i)
                    user = User.objects.get(email=tester.email)
                    transfer_pwg = TransferPwg(pwg_owner=pwg, pwgs_owner=pwgs, user=user)
                    transfer_pwg.save()
                    pwg.location = "T"
                    pwg.transfer_to = user
                    pwg.save()

                    # creating entry in PWG History table
                    if PWGHistory.objects.filter(object=user, pwg=pwg, action="T").exists():
                        pass
                    else:
                        pwg_his = PWGHistory(object=user, pwg=pwg, action="T")
                        pwg_his.save()

            return redirect("pwg-sublist", id=pwgs.id)
        elif accType == "user-home":
            for pkid in pk:
                if pkid == ",":
                    pass
                elif pkid == " ":
                    pass
                elif PWG.objects.filter(id=pkid).exists():
                    pwg_obj = PWG.objects.get(id=pkid)
                    pwgs = pwg_obj.owned_by

                    for user_id in tester_ids:
                        if user_id == ",":
                            pass
                        elif user_id == " ":
                            pass
                        elif WebUser.objects.filter(id=user_id).exists():
                            user_obj = WebUser.objects.get(id=user_id)
                            user_obj.is_authorized = True
                            main_user = user_obj.user

                            pwg_obj.user_location = "A"
                            pwg_obj.is_authorized = True
                            pwg_obj.save()
                            user_obj.save()

                            if Authorize.objects.filter(pwg=pwg_obj, authorize_to=main_user).exists():
                                pass
                            else:
                                authr = Authorize(pwg=pwg_obj, authorize_to=main_user, pwgserver=pwgs)
                                authr.save()

                            if PWGHistory.objects.filter(object=main_user, pwg=pwg_obj, action="A").exists():
                                pass
                            else:
                                pwg_his = PWGHistory(object=main_user, pwg=pwg_obj, action="A")
                                pwg_his.save()
                        else:
                            messages.error(request, "User object not found!")
                            return redirect("user-home")
                else:
                    messages.error(request, "PWG not found!")
                    return redirect("user-home")

            return redirect("user-home")
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

                        # creating entry in PWG histroy table
                        if PWGHistory.objects.filter(object=user, pwg=pwg, action="T").exists():
                            pass
                        else:
                            pwg_his = PWGHistory(object=user, pwg=pwg, action="T")
                            pwg_his.save()

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


def seller_list(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        seller = Seller.objects.all()
        seller_json = serializers.serialize('json', seller)

        return HttpResponse(seller_json, content_type='application/json')
    else:
        return JsonResponse({"data": False}, status=200)


def user_list(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        pk = request.GET.get("pk", None)
        if UserToUser.objects.filter(main_user=pk).exists():
            users = {}
            i = 0
            user_obj = UserToUser.objects.filter(main_user=pk)
            for obj in user_obj:
                u_id = obj.associated_user.id
                users[i] = WebUser.objects.get(id=u_id).first_name
                users[i+1] = WebUser.objects.get(id=u_id).id
                i += 2

            user_json = json.dumps(users)
            return HttpResponse(user_json, content_type='application/json')

        return JsonResponse({"data": False}, status=200)
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
            pwgs = pwg.owned_by
            usr = User.objects.get(is_superuser=True)
            pwg.transfer_to = usr
            pwg.save()

            if PWGHistory.objects.filter(object=usr, pwg=pwg, action="RAD").exists():
                pass
            else:
                pwg_his = PWGHistory(object=usr, pwg=pwg, action="RAD")
                pwg_his.save()

            if TransferPwg.objects.filter(pwg_owner=pwg).exists():
                pwg_trans = TransferPwg.objects.get(pwg_owner=pwg)
                pwg_trans.delete()

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
                if Share.objects.filter(share_to=current_user, pwg=pwg_object).exists():
                    print("not saved")
                else:
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

                        if PWGHistory.objects.filter(object=u, pwg=pwg_obj, action="A").exists():
                            pass
                        else:
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

                        if PWGHistory.objects.filter(object=u, pwg=pwg_obj, action="S").exists():
                            pass
                        else:
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

        elif accType == "user-user":
            # check for the pk in the database.
            if WebUser.objects.filter(id=pk).exists():
                my_object = WebUser.objects.get(id=pk)
                name = my_object.first_name
                if UserToUser.objects.filter(associated_user=pk).exists():
                    u_obj = UserToUser.objects.get(associated_user=pk)
                    u_obj.delete()

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
                if my_object.is_shared or my_object.is_authorized:
                    name = my_object.alias
                    name = "Oops, {} is not deleted because either the {} is shared or Authorized".format(name, name)
                    return JsonResponse({"msg": name}, status=200)
                my_object.transfer_to = None
                my_object.location = "A"
                my_object.sold_from = None
                name = my_object.alias
                s = name + " deleted"
                u = request.user
                u = User.objects.filter(Q(email=u) | Q(username=u))
                if PWGHistory.objects.filter(object=u, pwg=my_object, action="D").exists():
                    pass
                else:
                    s = PWGHistory(object=u, pwg=my_object, action="D")
                    s.save()

                name = "{} has been successfully deleted from your list".format(name)
                my_object.save()

                return JsonResponse({"msg": name}, status=200)
            else:
                # if name not found, then return msg
                return JsonResponse({"msg": False}, status=200)

        elif accType == "user-home":
            # check for the pk in the database.
            if PWG.objects.filter(id=pk).exists():
                my_object = PWG.objects.get(id=pk)
                if my_object.is_shared or my_object.is_authorized:
                    name = my_object.alias
                    name = "Oops, {} is not deleted because either the {} is shared or Authorized".format(name, name)
                    return JsonResponse({"msg": name}, status=200)
                my_object.user_location = None
                my_object.sold_from = None
                name = my_object.alias
                s = name + " deleted"
                u = request.user
                u = User.objects.filter(Q(email=u) | Q(username=u))
                if PWGHistory.objects.filter(object=u[0], pwg=my_object, action="D").exists():
                    name = 'something went wrong try again!'
                else:
                    s = PWGHistory(object=u[0], pwg=my_object, action="D")
                    s.save()

                    name = "{} has been successfully deleted from your list".format(name)
                    my_object.save()

                return JsonResponse({"msg": name}, status=200)
            else:
                # if name not found, then return msg
                return JsonResponse({"msg": False}, status=200)
    elif request.method == "POST":
        u = request.user
        u = User.objects.filter(Q(username=u) | Q(email=u))
        accType = request.POST.get("accType", None)
        pk = request.POST.get("pk", None)
        if accType == "multiple-pwg":
            temp_list = ''
            new_values = []
            for i in pk:
                if i == ",":
                    new_values.append(int(temp_list))
                    temp_list = ''
                elif i == " ":
                    pass
                else:
                    temp_list += i
            new_values.append(int(temp_list))

            for pwg_id in new_values:
                # check for the pk in the database.
                if PWG.objects.filter(id=pwg_id).exists():
                    my_object = PWG.objects.get(id=pwg_id)
                    if my_object.is_shared or my_object.is_authorized:
                        name = my_object.alias
                        messages.error(request, "Oops, {} is not deleted because either the {} is shared or Authorized".format(name, name))
                        return redirect("user-home")
                    my_object.user_location = None
                    my_object.sold_from = None
                    name = my_object.alias
                    s = name + " deleted"
                    u = request.user
                    u = User.objects.filter(Q(email=u) | Q(username=u))
                    if PWGHistory.objects.filter(object=u[0], pwg=my_object, action="D").exists():
                        pass
                    else:
                        s = PWGHistory(object=u[0], pwg=my_object, action="D")
                        s.save()

                    my_object.save()

                else:
                    # if name not found, then return msg
                    messages.error(request, "PWG Not found!")
                    return redirect("user-home")

            messages.error(request, "PWG successfully deleted!")
            return redirect("user-home")
        elif accType == "multiple-users":
            temp_list = ''
            new_values = []
            for i in pk:
                if i == ",":
                    new_values.append(int(temp_list))
                    temp_list = ''
                elif i == " ":
                    pass
                else:
                    temp_list += i
            new_values.append(int(temp_list))

            for user_id in new_values:
                # check for the pk in the database.
                if UserToUser.objects.filter(associated_user=user_id).exists():
                    user_obj = UserToUser.objects.get(associated_user=user_id)
                    my_object = WebUser.objects.get(id=user_id)
                    if my_object.is_shared or my_object.is_authorized:
                        name = my_object.alias
                        messages.error(request, "Oops, {} is not deleted because either the {} is shared or Authorized".format(name, name))
                        return redirect("user-user")

                    user_obj.delete()
                    my_object.associated_with = None
                    my_object.save()
                    print("deleted")

                else:
                    # if name not found, then return msg
                    messages.error(request, "Something went wrong, try again!")
                    return redirect("user-user")

            messages.error(request, "User successfully deleted!")
            return redirect("user-user")

    else:
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

                    if PWGHistory.objects.filter(object=user, pwg=pwg_obj, action="RAD").exists():
                        pass
                    else:
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
                        if pwg_obj.is_authorized or pwg_obj.is_freeze or pwg_obj.is_shared:
                            messages.info(request,
                                          " {} PWG is not transferred because either it is Authorized or Shared or Freezed".format(
                                              pwg_obj.alias))
                            return redirect('seller-pwg')
                        pwg_obj.sold_from = u
                        pwg_obj.user_location = "T"
                        pwg_obj.save()

                        if PWGHistory.objects.filter(object=u, pwg=pwg_obj, action="T").exists():
                            pass
                        else:
                            p = PWGHistory(object=u, pwg=pwg_obj, action="T")
                            p.save()

        return redirect("seller-pwg")

    else:
        messages.info(request, "something went wrong try again!")
        return redirect("/")


def testing_history(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the history from the database
        pk = request.GET.get("pk", None)
        # check for the pk in the database.

        if TesterPWGHistory.objects.filter(pwg_name=pk).exists():
                testing_his = TesterPWGHistory.objects.filter(pwg_name=pk)
                testing_his_json = serializers.serialize('json', testing_his)
                return HttpResponse(testing_his_json, content_type="application/json")
        else:
            return JsonResponse({"history": False}, status=200)

    return JsonResponse({}, status=400)


def retest(request):
    if request.method == "POST":
        pk = request.POST.get('values', None)
        accType = request.POST.get('accType', None)

        user = request.user
        user = User.objects.get(email=user)

        for pwg_id in range(len(pk)):
            if pk[pwg_id] == " ":
                pass
            elif pk[pwg_id] == ",":
                pass
            else:
                if PWG.objects.filter(id=pk[pwg_id]).exists():

                    pwg_obj = PWG.objects.get(id=pk[pwg_id])
                    pwg_obj.is_tested = False
                    pwg_obj.is_tested_good = False
                    pwg_obj.is_tested_faulty = False
                    pwg_obj.save()
                    if PWGHistory.objects.filter(object=user, pwg=pwg_obj, action="RT").exists():
                        pass
                    else:
                        pwg_his = PWGHistory(object=user, pwg=pwg_obj, action="RT")
                        pwg_his.save()

        if accType == "tester-home":
            return redirect("tester-home")

    else:
        messages.info(request, "something went wrong, Try again!")
        return redirect("/")


def custom_reset(request):
    email = request.GET['email']
    p = request.GET['password']
    u = User.objects.get(email=email)
    u.set_password(p)
    u.save()
    return HttpResponse("successfully changed!")


def fail(request):
    if request.method == "POST":
        pwg_id = request.POST.get('fail_pwg_value')
        if PWG.objects.filter(id=pwg_id):
            pwg_obj = PWG.objects.get(id=pwg_id)
            pwg_obj.is_tested = True
            pwg_obj.is_tested_faulty = True
            pwg_obj.is_tested_good = False
            pwg_alias = pwg_obj.alias

            user = pwg_obj.transfer_to
            pwg_obj.save()

            if PWGHistory.objects.filter(object=user, pwg=pwg_obj, action="F").exists():
                pass
            else:
                pwg_his = PWGHistory(object=user, pwg=pwg_obj, action="F")
                pwg_his.save()

            messages.info(request, "Successfully added the {} in failed list".format(pwg_alias))
            return redirect("tester-test")
        else:
            messages.error(request, "PWG object is not available")
            return redirect("tester-test")

    messages.error(request, "something went wrong! try again")
    return redirect("/")


def pass_pwg(request):
    if request.method == "POST":
        pwg_id = request.POST.get('pass_pwg_value')
        if PWG.objects.filter(id=pwg_id):
            pwg_obj = PWG.objects.get(id=pwg_id)
            pwg_obj.is_tested = True
            pwg_obj.is_tested_faulty = False
            pwg_obj.is_tested_good = True
            pwg_alias = pwg_obj.alias

            user = pwg_obj.transfer_to
            pwg_obj.save()

            if PWGHistory.objects.filter(object=user, pwg=pwg_obj, action="P").exists():
                pass
            else:
                pwg_his = PWGHistory(object=user, pwg=pwg_obj, action="P")
                pwg_his.save()

            messages.info(request, "Successfully added the {} in passed list".format(pwg_alias))
            return redirect("tester-test")
        else:
            messages.error(request, "PWG object is not available")
            return redirect("tester-test")

    messages.error(request, "something went wrong! try again")
    return redirect("/")


def destination(request):
    user_obj = request.user
    user_obj = User.objects.get(Q(email=user_obj) | Q(username=user_obj))
    user_email = user_obj.email
    if user_obj.is_authenticated:
        if WebAdmin.objects.filter(email=user_email).exists():
            return redirect("admin-home")
        elif Seller.objects.filter(email=user_email).exists():
            return redirect("seller-home")
        elif Tester.objects.filter(email=user_email).exists():
            return redirect("tester-home")
        elif WebUser.objects.filter(email=user_email).exists():
            return redirect("user-home")
    messages.error(request, "Login first then try again!!")
    return redirect("/")


def share_transfer_multiple(request):
    if request.method == "POST":
        user_ids = request.POST.get("tester_ids", None)
        pk = request.POST.get("pk", None)
        action = request.POST.get("action", None)
        new_values = []
        temp_list = ''

        for i in user_ids:
            if i == ",":
                new_values.append(int(temp_list))
                temp_list = ''
            elif i == " ":
                pass
            else:
                temp_list += i
        new_values.append(int(temp_list))
        user_ids = new_values
        new_values = []
        temp_list = ''

        for i in pk:
            if i == ",":
                new_values.append(int(temp_list))
                temp_list = ''
            elif i == " ":
                pass
            else:
                temp_list += i
        new_values.append(int(temp_list))
        pk = new_values

        for id_pwg in pk:
            if PWG.objects.filter(id=id_pwg).exists():
                pwg_obj = PWG.objects.get(id=id_pwg)
                pwgs = pwg_obj.owned_by
                if action == "share":
                    for user_id in user_ids:
                        if user_id == ",":
                            pass
                        elif user_id == " ":
                            pass
                        elif WebUser.objects.filter(id=user_id).exists():
                            user_obj = WebUser.objects.get(id=user_id)
                            user_obj.is_shared = True
                            main_user = user_obj.user

                            pwg_obj.user_location = "S"
                            pwg_obj.is_shared = True
                            pwg_obj.save()
                            user_obj.save()

                            if Share.objects.filter(share_to=main_user, pwg=pwg_obj).exists():
                                pass
                            else:
                                share_obj = Share(pwg=pwg_obj, share_to=main_user, pwgserver=pwgs)
                                share_obj.save()

                            if PWGHistory.objects.filter(object=main_user, pwg=pwg_obj, action="S").exists():
                                pass
                            else:
                                pwg_his = PWGHistory(object=main_user, pwg=pwg_obj, action="S")
                                pwg_his.save()
                        else:
                            messages.error(request, "User object not found!")
                            return redirect("user-home")
                elif action == "transfer":
                    if pwg_obj.is_authorized or pwg_obj.is_freeze or pwg_obj.is_shared:
                        messages.info(request,
                                      " {} PWG is not transferred because either it is Authorized or Shared or Freezed".format(
                                          pwg_obj.alias))
                        return redirect('user-home')
                    for user_id in user_ids:
                        if user_id == ",":
                            pass
                        elif user_id == " ":
                            pass
                        elif WebUser.objects.filter(id=user_id).exists():
                            user_obj = WebUser.objects.get(id=user_id)
                            main_user = user_obj.user

                            pwg_obj.user_location = "T"
                            pwg_obj.sold_from = main_user
                            pwg_obj.save()
                            user_obj.save()

                            if PWGHistory.objects.filter(object=main_user, pwg=pwg_obj, action="T").exists():
                                pass
                            else:
                                pwg_his = PWGHistory(object=main_user, pwg=pwg_obj, action="T")
                                pwg_his.save()

                        else:
                            messages.error(request, "User object not found!")
                            return redirect("user-home")
            else:
                messages.error(request, "PWG not found!")
                return redirect("user-home")

        return redirect("user-home")
    messages.error(request, "something went wrong, try again!")
    return redirect("user-home")


def passtext(request):
    if request.is_ajax and request.method == "GET":
        passText = request.GET.get("passText", None)
        pk = request.GET.get("pk", None)
        if PWG.objects.filter(id=pk).exists():
            pwg = PWG.objects.get(id=pk)
            pwg_use_password = PwgUseRecord(password=passText, pwg=pwg)
            pwg_use_password.save()
            return JsonResponse({"msg": "Saved"}, status=200)
    return JsonResponse({"msg": False}, status=200)


def simple_checkout(request):
    return render(request, "payment/checkout.html")


def assist_admin(request):
    return render(request, "tesafe/new-admin.html")


def chat_history(request):
    usr = request.user
    fk = request.GET.get('fk', None)
    if User.objects.filter(Q(username=usr) | Q(email=usr)).exists():
        usr = User.objects.get(Q(username=usr) | Q(email=usr))
        if MessageModel.objects.filter(user=usr, recipient=fk).exists():
            msgs = MessageModel.objects.filter(user=usr, recipient=fk)[:10]
            msgs = serializers.serialize('json', msgs)
            return HttpResponse(msgs, content_type="application/json")
        else:
            return JsonResponse({"history": False}, status=200)
    return JsonResponse({"history": False}, status=200)


def chat_multiple(request):
    if request.method == "POST":
        users = request.POST.get('users', None)
        accType = request.POST.get('accType', None)
        action = request.POST.get('action', None)
        new_values = []
        temp_list = ''

        for i in users:
            if i == ",":
                new_values.append(int(temp_list))
                temp_list = ''
            elif i == " ":
                pass
            else:
                temp_list += i
        new_values.append(int(temp_list))
        users = new_values
        new_values = ''
        temp_list = []
        count = 0
        if accType == "seller":
            for i in users:
                if Seller.objects.filter(id=i).exists():
                    count += 1
                    new_values += Seller.objects.get(id=i).first_name
                    new_values += ', '
                    temp_list.append(Seller.objects.get(id=i).email)
        elif accType == "tester":
            for i in users:
                if Tester.objects.filter(id=i).exists():
                    count += 1
                    new_values += Tester.objects.get(id=i).first_name
                    new_values += ', '
                    temp_list.append(Tester.objects.get(id=i).email)

        # trying to put ' , and' at last place
        new_values = new_values[:-2]
        removal = ","
        reverse_removal = removal[::-1]

        if count <= 2:
            replacement = " and "
        else:
            replacement = ", and "
        reverse_replacement = replacement[::-1]
        new_values = new_values[::-1].replace(reverse_removal, reverse_replacement, 1)[::-1]

        param = {
            "name": new_values,
            "selected_user": json.dumps(temp_list),
            "action": action,
        }
        return render(request, 'core/chat.html', param)


