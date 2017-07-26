from django.contrib.auth import models as auth_models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import ugettext_lazy as _
from config import settings
from music.models import Music

__all__ = (
    'MyUser',
    'Playlist',
    'PLMusics',
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        try:
            validate_email(email)
            user = self.model(
                email=self.normalize_email(email),
                username=username,
                # name=name,
            )
            user.set_password(password)
            user.save()
            return user
        except ValidationError:
            raise ValidationError('이메일 양식이 올바르지 않습니다.')

    def create_superuser(self, email, username, password=None):
        try:
            validate_email(email)
            user = self.create_user(
                email=email,
                username=username,
                # name=name,
                password=password,
            )
            user.is_admin = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            return user
        except ValidationError:
            raise ValidationError('이메일 양식이 올바르지 않습니다.')


# 사용자 정보 모델
class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Email ID',
        max_length=255,
        unique=True,
        null=True,
    )
    username = models.CharField(max_length=40, null=True, unique=True)
    first_name = models.CharField(max_length=20, default='')
    last_name = models.CharField(max_length=20, default='')
    # TODO img_profile - CustomImageField 설정 필요
    img_profile = models.ImageField(upload_to='member', blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_superuser = models.BooleanField(default=False)
    # name = models.CharField(max_length=100, default="")

    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return "username: {}".format(self.username if self.username else self.email)

    @property
    def is_staff(self):
        """일반 사용자인지 아니면 스태프 권한이 있는지?"""
        return self.is_admin

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def has_module_perms(self, app_label):
        """user가 주어진 app_label에 해당하는 권한이 있는지, has_perm과 비슷"""
        if self.is_active and self.is_superuser:
            return True
        return auth_models._user_has_module_perms(self, app_label)

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True

        return auth_models._user_has_perm(self, perm, obj)

    def get_full_name(self):
        return self.email if self.email else self.username

    def get_short_name(self):
        return self.email if self.email else self.username


# 유저별 플레이리스트 모델
class Playlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name_playlist = models.CharField(max_length=30, default='playlist')
    playlist_musics = models.ManyToManyField(
            Music,
            through='PLMusics',
            related_name='playlist_musics'
        )


# 유저의 플레이리스트 내 음악 목록 모델
class PLMusics(models.Model):
    name_playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)