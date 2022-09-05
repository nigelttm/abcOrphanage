from email.policy import default
from typing_extensions import Required
from attr import field
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from requests import request
from abcApp.models import Donation, MoneyDonation, Request, Upload, User, Visit

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('user_id', 'password1', 'password2')
        
    def clean_user_id(self):
        username = self.cleaned_data['user_id']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(user_id=username)

        except User.DoesNotExist:
            return username
        
        raise forms.ValidationError('Username "%s" is already in use.' % username)
        
    def clean_validate_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if (password1==password2):
            return password1
        raise forms.ValidationError('The two password fields didn’t match.')
    
class AdminSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('user_id', 'password1', 'password2', 'role')
        
    def clean_user_id(self):
        username = self.cleaned_data['user_id']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(user_id=username)

        except User.DoesNotExist:
            return username
        
        raise forms.ValidationError('Username "%s" is already in use.' % username)
        
    def validate_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if (password1==password2):
            return password1
        raise forms.ValidationError('The two password fields didn’t match.')
    


class UserAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('user_id', 'password')

    def clean(self):
        if self.is_valid():
            user_id = self.cleaned_data['user_id']
            password = self.cleaned_data['password']
            if not authenticate(username=user_id, password=password):
                raise forms.ValidationError("Invalid login")



class UserUpdateForm(forms.ModelForm):
    user_id = forms.CharField(required=False)
    newPass = forms.CharField(required=False)
    currPass = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('newPass', 'currPass')

    def clean(self):
        print(self)
        if self.is_valid():
            user_id = self.cleaned_data['user_id']
            password = self.cleaned_data['currPass']
            if not authenticate(username=user_id, password=password):
                raise forms.ValidationError("Incorrect Password")

    def save(self, user):
        user.save()
        return user

class RequestCreationForm(forms.ModelForm):
    request_Text = forms.CharField(required=False)
    request_Obj = forms.CharField(required=True)
    isPerm = forms.BooleanField(required=False)

    class Meta:
        model = Request
        fields = ('request_Text', 'request_Obj', 'isPerm')
        
class RequestDonationForm(forms.ModelForm):
    user = forms.CharField(required=True)
    donation_type = forms.CharField(required=True)
    delivery_date = forms.DateField(required=False)

    class Meta:
        model = Donation
        fields = ('donation_type', 'user', 'delivery_date')

class VisitCreationForm(forms.ModelForm):
    reason = forms.CharField(required=True)
    visit_date = forms.DateField(required=True)
    qty = forms.IntegerField(required=True, min_value=1, max_value=100)

    class Meta:
        model = Visit
        fields = ('visit_date', 'reason', 'qty')

class WorkCreationForm(forms.ModelForm):
    upload_name = forms.CharField(required=True)
    child_object = forms.FileField(required=True)

    class Meta:
        model= Upload
        fields = ('upload_name','child_object',)

class DonationCreationForm(forms.ModelForm):
    yearly = forms.BooleanField(required=False)

    class Meta:
        model = MoneyDonation
        fields = ('yearly',)