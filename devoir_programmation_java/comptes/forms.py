from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm
from .models import Compte
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class RegistrationForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control','type':'text','name': 'username'}),
        label="username")
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control','type':'text','name': 'email'}),
        label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name':'password1'}),
        label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name': 'password2'}),
        label="Password (again)")
    type_cmp= forms.CharField(widget=forms.HiddenInput())

    '''added attributes so as to customise for styling, like bootstrap'''
    class Meta:
        model = Compte
        fields = ['username','email','password1','password2','type_cmp']
        field_order = ['username','email','password1','password2']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please try again!")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm,self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class RegistrationFormAdmin(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control','type':'text','name': 'username'}),
        label="username")
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control','type':'text','name': 'email'}),
        label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name':'password1'}),
        label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name': 'password2'}),
        label="Password (again)")
    type_cmp= forms.CharField(widget=forms.HiddenInput(attrs={'value':'Enseignant'}),
        label="type_cmp")

    '''added attributes so as to customise for styling, like bootstrap'''
    class Meta:
        model = Compte
        fields = ['username','email','password1','password2','type_cmp']
        field_order = ['username','email','password1','password2']

    def clean(self):
        cleaned_data = super(RegistrationFormAdmin, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please try again!")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationFormAdmin,self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

#The save(commit=False) tells Django to save the new record, but dont commit it to the database yet
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = Compte
        fields = ('email', 'username', 'type_cmp', 'password', 'is_active', 'is_superuser')
class FormAuthentication(forms.Form): # Note: forms.Form NOT forms.ModelForm
    """email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control','type':'text','name': 'email','placeholder':'Email'}), 
        label='Email')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name': 'password','placeholder':'Password'}),
        label='Password')"""
    email = forms.EmailField(max_length=60, help_text = 'Required. Add a valid email address')
    password  = forms.CharField(label= 'Password', widget=forms.PasswordInput)

    class Meta:
        model = Compte
        fields =  ('email', 'password')
        widgets = {
                   'email':forms.TextInput(attrs={'class':'form-control'}),
                   'password':forms.TextInput(attrs={'class':'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        """
          specifying styles to fields 
        """
        super(FormAuthentication, self).__init__(*args, **kwargs)
        for field in (self.fields['email'],self.fields['password']):
            field.widget.attrs.update({'class': 'form-control '})

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login')
