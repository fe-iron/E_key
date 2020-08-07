from django.shortcuts import render, redirect
from .models import WebAdmin, Seller, Tester
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.utils import timezone






# Create your views here.
def index(request):
    if request.method == 'POST':
        accType = request.POST['accType']
        password = request.POST['password']
        uname = request.POST['uname']

        # user = auth.authenticate(username=uname, password=password)
        # if user is not None:
        #     auth.login(request, user)
        #     messages.info(request, "Successfully Logged in ")



        # else:
        #     messages.info(request, 'Invalid user id and password')
        #     return redirect('/')
        if accType == 'admin':
            return admin_home(request)
        elif accType == 'seller':
            return seller_home(request)
        elif accType == 'tester':
            return render(request, 'tester/tester-home.html', {'num': [11, 23, 33, 42, 35, 67, 78, 49, 10]})
        elif accType == 'user':
            return render(request, 'tesafe/admin-home.html', {'num': [11, 23, 33, 42, 35, 67, 78, 49, 10]})


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
                    user = User.objects.create_user(username=uname, first_name=fname, last_name=lname, email=email, password=password1)
                    user.save()

                    webAdmin = WebAdmin(user=user, first_name=fname, last_name=lname, email=email, phone=phone)
                    webAdmin.save()

                    return render(request, 'tesafe/admin-home.html')


                elif accType == 'seller':

                    user = User.objects.create_user(username=uname, first_name=fname, last_name=lname, email=email, password=password1)
                    user.save()

                    seller = Seller(user=user, first_name=fname, last_name=lname, email=email, phone=phone)
                    seller.save()

                    return render(request, 'seller/seller-home.html')

                elif accType == 'tester':

                    user = User.objects.create_user(username=uname, first_name=fname, last_name=lname, email=email,
                                                    password=password1)
                    user.save()

                    tester = Tester(user=user, first_name=fname, last_name=lname, email=email, phone=phone)
                    tester.save()

                    return render(request, 'tester/tester-home.html')

            elif accType == 'user':
                    pass
        else:
            messages.error(request, "Password do not match! try again")
            return redirect('register')

    return render(request, 'tesafe/register.html')


def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
    print("active session: ",user_id_list)

    return User.objects.filter(id__in=user_id_list)


def admin_home(request):
    admin_count = WebAdmin.objects.all().count()
    seller_count = Seller.objects.all().count()
    queryset = get_current_users()
    params = {
        'admin_count': admin_count,
        'seller_count': seller_count,
        'num': [11, 23, 33, 42, 35, 67, 78, 49, 10],
        'seller_online': queryset.count()
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



def names_view(request):
    ctx = {}
    url_parameter = request.GET.get("q")

    if url_parameter:
        name = Names.objects.filter(name__icontains=url_parameter)
    else:
        name = Names.objects.all()

    ctx["Name"] = name
    if request.is_ajax():

        html = render_to_string(
            template_name="artists-results-partial.html", context={"name": name}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    return render(request, "tesafe/admin-home.html", context=ctx)



def tester_home(request):
    return render(request, 'tester/tester-home.html')


def tester_test(request):
    return render(request, 'tester/tester-test.html')