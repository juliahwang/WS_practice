from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from member.models import MyUser


class UserCreationForm(forms.ModelForm):
    """
    유저 생성폼.
    """
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
            'password',
            'username',
            'is_active',
            'is_admin',
        )

    def clean_password(self):
        return self.initial["password"]
