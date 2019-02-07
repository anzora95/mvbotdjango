from django import forms
from django.contrib.auth.models import User


from InstabotMV.models import Creds, List_Tag, UsList, HashtagList, Media
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class GenerateRandomUserForm(forms.Form):
    total = forms.IntegerField(
        validators=[
            MinValueValidator(50),
            MaxValueValidator(500)
        ]
    )

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())


class CreateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20, error_messages={
        'required': 'The field is required',
        'invalid': 'Enter a valid name'
    })
    last_name = forms.CharField(max_length=20, error_messages={
        'required': 'The field is required',
        'invalid': 'Enter a valid last name'
    })
    username = forms.CharField(max_length=20, error_messages={
        'required': 'The username field is required',
        'unique': 'The username is already taken',
        'invalid': 'Enter a valid username'
    })
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(), error_messages={
        'required': 'The password is required'
    })
    email = forms.CharField(error_messages={
        'required': 'The email is required',
        'unique': 'The email is already associated with an account',
        'invalid': 'Enter a valid email'
    })

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email')


class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=20, error_messages={
        'required': 'The username field is required',
        'unique': 'The username is already taken',
        'invalid': 'Enter a valid username'
    })
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(), error_messages={
        'required': 'The password field is required'
    })
    email = forms.CharField(error_messages={
        'required': 'The email field is required',
        'unique': 'The email is already associated with an account',
        'invalid': 'Enter a valid email'
    })


class InstaCredsForm(forms.ModelForm):
    insta_user = forms.CharField(max_length=30, error_messages={
        'required': 'The username field is required',
        'unique': 'The username entered is already in our records',
        'invalid': 'Enter a valid username'
    })
    insta_pass = forms.CharField(max_length=20, widget=forms.PasswordInput(), error_messages={
        'required': 'The password field is required'
    })

    class Meta:
        model = Creds
        fields = ('insta_user', 'insta_pass',)


class TaglistForm(forms.ModelForm):
    insta_tag = forms.CharField(error_messages={
        'required': 'Please insert some data',
    })

    class Meta:
        model = List_Tag
        fields = ('insta_tag',)


class UserlistForm(forms.ModelForm):
    insta_us_name = forms.CharField(error_messages={
        'required': 'Please insert some data',
    })

    class Meta:
        model = UsList
        fields = ('insta_us_name',)


class CommandForm(forms.Form):
    command = forms.CharField(max_length=200)


class CombosTagPadre(forms.Form):
    tag_padre = forms.ModelChoiceField(queryset=Media.objects.all())


class ComboTagHijo(forms.Form):
    tag = forms.CharField(label = 'Puntos a sumar', max_length=100, initial='follow, me', required=True)









