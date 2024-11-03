from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Mailing


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailings/mailings_list.html'


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailings/mailings_detail.html'


class MailingCreateView(CreateView):
    model = Mailing
    fields = ['email', 'full_name', 'comment']
    template_name = 'mailings/mailings_form.html'
    success_url = reverse_lazy('mailings_list')


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['email', 'full_name', 'comment']
    template_name = 'mailings/mailings_form.html'
    success_url = reverse_lazy('mailings_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailings/mailings_confirm_delete.html'
    success_url = reverse_lazy('mailings_list')
