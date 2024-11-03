from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Message


class MessageListView(ListView):
    model = Message
    template_name = 'message_list/message_list.html'


class MessageDetailView(DetailView):
    model = Message
    template_name = 'message_list/message_detail.html'


class MessageCreateView(CreateView):
    model = Message
    fields = ['email', 'full_name', 'comment']
    template_name = 'message_list/message_form.html'
    success_url = reverse_lazy('message_list')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ['email', 'full_name', 'comment']
    template_name = 'message_list/message_form.html'
    success_url = reverse_lazy('message_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'message_list/message_confirm_delete.html'
    success_url = reverse_lazy('message_list')
