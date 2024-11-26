from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from config.forms.forms import MessageForm
from .models import Message


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messages_list/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        # Проверяем, принадлежит ли пользователь к группе "менеджеров"
        if self.request.user.groups.filter(name='Managers').exists():
            # Если принадлежит к группе "менеджеры", показываем все клиенты
            return Message.objects.all().order_by('subject')
        else:
            # Если не принадлежит, показываем только клиенты текущего пользователя
            return Message.objects.filter(owner=self.request.user).order_by('subject')


class MessageDetailView(DetailView):
    model = Message
    template_name = 'messages_list/message_detail.html'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'messages_list/message_form.html'
    success_url = reverse_lazy('messages:message_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = False  # Для создания клиента
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'messages_list/message_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True  # Для редактирования клиента
        return context

    def get_object(self):
        client = get_object_or_404(Message, id=self.kwargs['pk'])
        if not client.is_owned_by(self.request.user):
            raise Http404("Вы не можете редактировать этот клиент.")
        return client

    def test_func(self):
        # Проверка, что пользователь имеет доступ
        return self.get_object().is_owned_by(self.request.user)

    def get_success_url(self):
        """
        Переопределение метода редиректа после успешного изменения статьи
        """
        return reverse('messages:message_detail', kwargs={'pk': self.object.pk})


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'messages_list/message_confirm_delete.html'
    success_url = reverse_lazy('messages:message_list')
