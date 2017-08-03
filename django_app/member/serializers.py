from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.core.validators import validate_email
from rest_framework import serializers


User = get_user_model()


class UserListSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'img_profile',
            'password',
            'is_active',
            'is_admin',
        )


class UserLoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )

    # def validate(self, data):
    #     email = data['email']
    #     password = data['password']
    #     is_active = data['is_active']
    #     user = authenticate(
    #         email=email,
    #         password=password,
    #         is_active=is_active,
    #     )
    #     if user is not None:
    #         self.data['user'] = user
    #     elif not is_active:
    #         raise serializers.ValidationError(
    #             'Please confirm your email to activate the account.'
    #         )
    #     else:
    #         raise serializers.ValidationError(
    #             'Login credentials not valid. Please try again.'
    #         )
    #     print(data)
    #     return data
