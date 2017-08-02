from django.contrib.auth import get_user_model, authenticate
from django.core.validators import validate_email
from rest_framework import serializers


User = get_user_model()


class UserLoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )

    def validate_email(self, data):
        email = data['email']
        if email and validate_email(email):
            pass


    def validate(self, data):
        email = data['email']
        password = data['password']
        is_active = data['is_active']
        user = authenticate(
            email=email,
            password=password
        )
        if user is not None:
            self.data['user'] = user
        elif not is_active:
            raise serializers.ValidationError(
                'Please confirm your email to activate the account.'
            )
        else:
            raise serializers.ValidationError(
                'Login credentials not valid. Please try again.'
            )
        return data
