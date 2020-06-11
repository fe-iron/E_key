# from django.contrib.auth.forms import UserCreationForm
# from django.db import transaction
# from .models import User, WebAdmin, Seller
# from django import forms
#
# class SellerSignUpForm(UserCreationForm):
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)
#     phone_number = forms.CharField(required=True)
#     email = forms.CharField(required=True)
#
#     class Meta(UserCreationForm.Meta):
#         model = User
#
#     @transaction.atomic
#     def data_save(self):
#         user = super().save(commit=False)
#         user.is_seller = True
#         user.is_staff = True
#         user.first_name = self.cleaned_data.get('first_name')
#         user.last_name = self.cleaned_data.get('last_name')
#         user.save()
#
#         seller = Seller.objects.create(user=user)
#         seller.phone = self.cleaned_data.get('phone_number')
#         seller.email = self.cleaned_data.get('email')
#
#         seller.save()
#         return seller
#
#
#
#
#
# class WebAdminSignUpForn(UserCreationForm):
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)
#     phone_number = forms.CharField(required=True)
#     email = forms.CharField(required=True)
#
#     class Meta(UserCreationForm.Meta):
#         model = User
#
#
#     @transaction.atomic
#     def data_save(self):
#         user = super().save(commit=False)
#         user.is_webAdmin = True
#         user.first_name = self.cleaned_data.get('first_name')
#         user.last_name = self.cleaned_data.get('last_name')
#         user.save()
#
#         webadmin = WebAdmin.objects.create(user=user)
#         webadmin.phone = self.cleaned_data.get('phone_number')
#         webadmin.email = self.cleaned_data.get('email')
#
#         webadmin.save()
#         return webadmin
