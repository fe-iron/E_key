from django.shortcuts import render
from django.views.generic import CreateView
# from .form import WebAdminSignUpForn, SellerSignUpForm
# from .models import WebAdmin, Seller, User
from django.contrib.auth.models import auth
from django.contrib import messages
# Create your views here.

def index(request):
    if request.method == 'POST':
        accType = request.POST['accType']
        password = request.POST['password']
        email = request.POST['email']

        if accType == 'admin':
            pass
        elif accType == 'seller':
            pass
        elif accType == 'Tester':
            pass
        elif accType == 'user':
            pass
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
