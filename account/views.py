from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse

from account.models import User
from account.serializers import (
    RegistrationSerializer,
    LoginSerializer,
    PasswordResetSerializer,
)
from account.utils import send_activation_email, send_password_reset_email


def index(request):
    return render(request, 'account/home.html')

class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save(is_active=False)

        # UID and Token
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Build activation URL with request
        activation_path = reverse("activate", kwargs={"uidb64": uidb64, "token": token})
        activation_url = request.build_absolute_uri(activation_path)

        # Send email
        send_activation_email(user.email, activation_url)

        return Response(
            {
                "message": "Registration successful. Please check your email to activate your account.",
                "user": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class ActivateAccountAPIView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if user.is_active:
                return Response(
                    {"detail": "This account already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response(
                    {"detail": "Your account has been successfully activated"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"detail": "Invalid Activation Link"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"detail": "Invalid activation link"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Implement throttling for the rate limiting later
class ResendActivationLinkAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                {"detail": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "User with this email does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.is_active:
            return Response(
                {"detail": "This account is already active. Login for access"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        activation_path = reverse(
            "activation", kwargs={"uidb64": uidb64, "token": token}
        )
        activation_url = request.build_absolute_url(activation_path)

        send_activation_email(user.email, activation_url)

        return Response(
            {"detail": "Activation URL has been resent"}, status=status.HTTP_200_OK
        )


class LoginAPIView(APIView):
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {"detail": "Account is Inactive. Please activate your account"},
                status=status.HTTP_403_FORBIDDEN,
            )

        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)

            login(request, user)
            return Response(
                {
                    "detail": "Login Successful",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"detail": "Invalide email or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class PasswordResetAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()

        if user:
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = default_token_generator.make_token(user)

            frontend_reset_url = (
                f"https://your-frontend.com/reset-password/confirm/{uidb64}/{token}/"
            )

            # For the case if we use django frontend
            # reset_url = reverse(
            #     "password_reset_confirm", kwargs={"uidb64": uidb64, "token": token}
            # )
            # absolute_reset_url = f"{request.build_absolute_url(reset_url)}"

            send_password_reset_email(user.email, frontend_reset_url)

            # It is the task of frontend to send it back to the view of PasswordResetConfirmView

        # 🛡️ Don't leak user existence information
        return Response(
            {"detail": "If a user with this email exists, a reset link has been sent."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"detail": "Invalid reset link."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Reset Link has been expired or is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        form = SetPasswordForm(user, request.data)

        if form.is_valid():
            form.save()
            return Response(
                {"detail": "Password is reset successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail - Form errors": form.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
