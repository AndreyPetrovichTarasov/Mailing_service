from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from config.forms.forms import MessageForm
from .models import Message


class MessageListView(ListView):
    model = Message
    template_name = 'messages_list/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.order_by('subject')


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


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'messages_list/message_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True  # Для редактирования клиента
        return context

    def get_success_url(self):
        """
        Переопределение метода редиректа после успешного изменения статьи
        """
        return reverse('messages:message_detail', kwargs={'pk': self.object.pk})


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'messages_list/message_confirm_delete.html'
    success_url = reverse_lazy('messages:message_list')
