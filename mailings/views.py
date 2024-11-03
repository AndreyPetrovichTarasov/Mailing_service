from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Mailing, MailingAttempt
from config.forms.forms import MailingForm
from django.views import View
from .services import send_mailing


def send_mailing_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    send_mailing(mailing)  # Запускаем отправку
    # Перенаправляем на страницу статуса рассылки
    return redirect(reverse('mailings:mailing_status', args=[pk]))


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailings/mailings_list.html'
    context_object_name = 'mailings'


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailings/mailings_detail.html'


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = False  # Для создания клиента
        return context


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True  # Для редактирования клиента
        return context

    def get_success_url(self):
        """
        Переопределение метода редиректа после успешного изменения статьи
        """
        return reverse('mailings:mailing_detail', kwargs={'pk': self.object.pk})


class MailingConfirmSendView(DetailView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_send.html'


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailings/mailings_confirm_delete.html'
    success_url = reverse_lazy('mailings_list')


class MailingSendView(View):
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

        # Проверка статуса перед отправкой
        if mailing.status == 'Запущена':
            messages.warning(request, "Рассылка уже запущена.")
        else:
            # Запускаем отправку
            send_mailing(mailing)
            mailing.status = 'Запущена'
            mailing.save()
            messages.success(request, "Рассылка успешно отправлена.")

        return redirect(reverse('mailings:mailing_status', args=[pk]))


class MailingStatusView(DetailView):
    model = Mailing
    template_name = 'mailings/mailing_status.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем все попытки отправки для данной рассылки
        context['attempts'] = MailingAttempt.objects.filter(mailing=self.object)
        return context
