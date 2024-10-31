from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import Serializer, IntegerField

from apps.users.models import User


class EmailModelSerializer(Serializer):
    email = CharField(max_length=255)


class VerifyEmailSerializer(Serializer):
    email = CharField(max_length=255)
    code = IntegerField()

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')

        cache_data = cache.get(email)
        if cache_data is None:
            raise ValidationError('Verification code expired.')

        if isinstance(cache_data, int):
            if code != cache_data:
                raise ValidationError('Code is incorrect.')
        else:
            if code != cache_data.get('code'):
                raise ValidationError('Code is incorrect.')

        return attrs


class ResetPasswordSerializer(Serializer):
    email = CharField(max_length=255)
    new_password = CharField(write_only=True)
    confirm_password = CharField(write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return attrs

    def save(self, **kwargs):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        user.set_password(self.validated_data['new_password'])
        user.save()
