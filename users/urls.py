from django.urls import path, reverse_lazy
from clients.views import ClientListView, AllClientListView, ClientUpdateView
from mailings.views import MailingListView, MailingUpdateView, AllMailingListView, DisableMailingView
from .views import RegisterView, CustomLoginView, ProfileEditView, email_verifixation, ProfileView, BlockUserView, \
    UsersListView, ActivateUserView, DeactivateUserView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='edit_profile'),
    path('confirm-registration/<str:token>/', email_verifixation, name='confirm-registration'),
    path('password-reset/', PasswordResetView.as_view(
        template_name='users/password_reset_form.html', email_template_name='users/password_reset_email.html',
        success_url=reverse_lazy('users:password_reset_done')
    ), name='password_reset'),

    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),

    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html', success_url=reverse_lazy('users:password_reset_complete')
    ), name='password_reset_confirm'),

    path('password-reset/complete/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),

    path('users/', UsersListView.as_view(), name='users_list'),
    path('activate/<int:pk>/', ActivateUserView.as_view(), name='activate_user'),
    path('deactivate/<int:pk>/', DeactivateUserView.as_view(), name='deactivate_user'),

    path('clients/', ClientListView.as_view(), name='client_list'),
    path('client/edit/<int:pk>/', ClientUpdateView.as_view(), name='client_edit'),
    path('clients/all/', AllClientListView.as_view(), name='all_clients'),

    # Страницы для рассылок
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/edit/<int:pk>/', MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailings/all/', AllMailingListView.as_view(), name='all_mailings'),

    # Для блокировки пользователя и отключения рассылки
    path('block_user/<int:user_id>/', BlockUserView.as_view(), name='block_user'),
    path('disable_mailing/<int:mailing_id>/', DisableMailingView.as_view(), name='disable_mailing'),
]
