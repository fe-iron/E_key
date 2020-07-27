from django.shortcuts import render
from django.views.generic import CreateView
# from .form import WebAdminSignUpForn, SellerSignUpForm
from .models import Names
from django.contrib.auth.models import auth
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
# Create your views here.

def index(request):
    if request.method == 'POST':
        accType = request.POST['accType']
        password = request.POST['password']
        email = request.POST['email']
        print(accType)
        if accType == 'admin':
            return render(request, 'tesafe/admin-home.html', {'num': [11,23,33,42,35,67,78,49,10]})
        elif accType == 'seller':
            return render(request, 'seller/seller-home.html', {'num': [11,23,33,42,35,67,78,49,10]})
        elif accType == 'Tester':
            return render(request, 'tesafe/admin-home.html', {'num': [11,23,33,42,35,67,78,49,10]})
        elif accType == 'user':
            return render(request, 'tesafe/admin-home.html', {'num': [11,23,33,42,35,67,78,49,10]})
        else:
            return render(request, 'tesafe/admin-home.html', {'num': [11,23,33,42,35,67,78,49,10]})
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



        if accType == 'admin':
            if password1 == password2:
                user = User.objects.create_user(username=uname, first_name=fname, last_name=lname, email=email, password=password1, is_webAdmin=True)
                user.save()

                webAdmin = WebAdmin(user=user, phone=phone, email=email)
                webAdmin.save()
                msg = messages.info("Account successfully created!")
                return render(request, 'tesafe/admin-page.html', {'msg': msg})

            else:
                msg = messages.error(request,"Password do not match! try again")
                return render(request, 'tesafe/admin-page.html', {'msg': msg})
        elif accType == 'seller':
            pass
        elif accType == 'Tester':
            pass
        elif accType == 'user':
            pass

    return render(request, 'tesafe/register.html')


def admin_home(request):
    return render(request, 'tesafe/admin-home.html', {'num': [11,23,33,42,35,67,78,49,10]})


def admin_seller(request):
    return render(request, 'tesafe/admin-seller.html', {'num': [11,23,33,42,35,67,78,49,10]})


def admin_tester(request):
    return render(request, 'tesafe/admin-tester.html', {'num': [11,23,33,42,35,67,78,49,10]})


def admin_info_server(request):
    return render(request, 'tesafe/admin-info-server.html', {'num': [11, 23, 33, 42, 35, 67, 78, 49, 10]})
# class webAdmin_register(CreateView):
#     model = User
#     form_class = WebAdminSignUpForn
#     template_name = 'tesafe/register.html'


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


def seller_authorized(request):
    return render(request, 'seller/seller-authorized.html')


def seller_shared(request):
    return render(request, 'seller/seller-shared.html')


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

