from random import randint

from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.serializers import EmailModelSerializer, VerifyEmailSerializer, ResetPasswordSerializer
from apps.users.tasks import send_to_email


@extend_schema(tags=["Password Reset"])
class SendResetEmailAPIView(GenericAPIView):
    serializer_class = EmailModelSerializer

    @extend_schema(
        summary="Send Password Reset Email",
        description="Sends a password reset code to the user's email.",
        responses={200: {"message": "Code sent successfully"}}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']
        code = randint(1000, 9999)
        cache.set(email, {'code': code}, timeout=6000)

        message = f"Your password reset code is {code}"
        send_to_email.delay(message, email)

        print(f"Email: {email}, code: {code}")
        return Response({"message": "Code sent successfully"})


@extend_schema(tags=["Password Reset"])
class VerifyEmailCodeAPIView(GenericAPIView):
    serializer_class = VerifyEmailSerializer

    @extend_schema(
        summary="Verify Email Code",
        description="Verifies the code sent to the user's email for password reset.",
        responses={200: {"message": "Code verified, proceed to reset password."}}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        return Response({"message": "Code verified, proceed to reset password."})


@extend_schema(tags=["Password Reset"])
class ResetPasswordAPIView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    @extend_schema(
        summary="Reset Password",
        description="Resets the user's password after verification.",
        responses={200: {"message": "Password reset successfully"}}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response({"message": "Password reset successfully"})
