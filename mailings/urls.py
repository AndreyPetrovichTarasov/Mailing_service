from django.urls import path
from mailings.apps import MailingsConfig
from .views import MailingCreateView, MailingDeleteView, MailingUpdateView, MailingDetailView, MailingListView

app_name = MailingsConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
]
