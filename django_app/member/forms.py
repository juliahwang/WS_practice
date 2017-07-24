from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import validate_email

from member.models import MyUser


class UserCreationForm(forms.ModelForm):
    """
    유저 생성폼.
    """
    email = forms.EmailField(
        label='email',
        widget=forms.EmailInput,
    )
    username = forms.CharField(
        label='username',
        widget=forms.TextInput,
    )
    img_profile = forms.ImageField(
        label='img_profile',
        widget=forms.FileInput,
    )
    password1 = forms.CharField(
        label='password1',
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='password2',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = MyUser
        fields = (
            'email',
            'username',
            'img_profile',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and validate_email(email):
            return email
        elif email and MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError('이미 가입된 이메일입니다.')
        else:
            raise forms.ValidationError('이메일 양식이 올바르지 않습니다.')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and MyUser.objects.filter(username=username).exists():
            raise forms.ValidationError('다른 사용자가 사용하고 있는 이름입니다.')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다. 다시 입력해주세요.')
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    User 업데이트 폼
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = (
            'email',
            'img_profile',
            'password',
            'username',
            'is_active',
            'is_admin',
        )

    def clean_password(self):
        return self.initial["password"]
