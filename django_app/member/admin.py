from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import UserChangeForm, UserCreationForm
from .models import MyUser


class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = (
        'email',
        'username',
        'is_admin',
    )
    list_filter = (
        'is_admin',
    )
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    # User 생성시 필요한 필드셋 정의
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')
        })
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(MyUser, MyUserAdmin)
admin.site.unregister(Group)