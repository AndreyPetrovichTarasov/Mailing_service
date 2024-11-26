import secrets

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from .forms import CustomUserCreationForm, UserProfileForm
from .models import CustomUser
from config.settings import EMAIL_HOST_USER


class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/confirm-registration/{token}/"
        send_mail(
            subject="Подтверждение регистрации на Perfect Mailing",
            message=f"Здравствуйте! Для подтверждения регистрации перейдите по ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verifixation(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    success_url = reverse_lazy("catalog:home")


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = "users/profile.html"


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = "users/edit_profile.html"
    success_url = reverse_lazy("home")  # Перенаправление после успешного сохранения

    def get_object(self, queryset=None):
        return self.request.user


class MyPasswordResetView(PasswordResetView):
    template_name = "users/password_reset_form.html"
    success_url = "users:password_reset_done"


class BlockUserView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        # Проверка, что пользователь является менеджером
        return self.request.user.is_staff

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        user.is_active = False
        user.save()
        return redirect("users:user_list")


class UsersListView(ListView):
    model = CustomUser
    template_name = "users/users_list.html"
    context_object_name = "users"


class ActivateUserView(UserPassesTestMixin, View):
    def test_func(self):
        # Проверяем, является ли пользователь менеджером
        return self.request.user.groups.filter(name="Managers").exists()

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.is_active = True
        user.save()
        messages.success(request, f"Пользователь {user.username} был активирован.")
        return redirect("users:users_list")  # Измените на ваш URL списка пользователей


# Представление для деактивации пользователя
class DeactivateUserView(UserPassesTestMixin, View):
    def test_func(self):
        # Проверяем, является ли пользователь менеджером
        return self.request.user.groups.filter(name="Managers").exists()

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.is_active = False
        user.save()
        messages.success(request, f"Пользователь {user.username} был деактивирован.")
        return redirect("users:users_list")
