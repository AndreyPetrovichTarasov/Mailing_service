from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from config.forms.forms import ClientForm

from .models import Client


@method_decorator(cache_page(60 * 15), name='dispatch')
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "clients/client_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        # Проверяем, принадлежит ли пользователь к группе "менеджеров"
        if self.request.user.groups.filter(name="Managers").exists():
            # Если принадлежит к группе "менеджеры", показываем все клиенты
            return Client.objects.all().order_by("full_name")
        else:
            # Если не принадлежит, показываем только клиенты текущего пользователя
            return Client.objects.filter(owner=self.request.user).order_by("full_name")


@method_decorator(cache_page(60 * 15), name='dispatch')
class ClientDetailView(DetailView):
    model = Client
    template_name = "clients/client_detail.html"


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:client_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = False  # Для создания клиента
        return context

    def form_valid(self, form):
        # Устанавливаем владельцем текущего пользователя
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = True  # Для редактирования клиента
        return context

    def get_success_url(self):
        """
        Переопределение метода редиректа после успешного изменения статьи
        """
        return reverse("clients:client_detail", kwargs={"pk": self.object.pk})

    def get_object(self):
        client = get_object_or_404(Client, id=self.kwargs["pk"])
        if not client.is_owned_by(self.request.user):
            raise Http404("Вы не можете редактировать этот клиент.")
        return client

    def test_func(self):
        # Проверка, что пользователь имеет доступ
        return self.get_object().is_owned_by(self.request.user)


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "clients/client_confirm_delete.html"
    success_url = reverse_lazy("clients:client_list")


class AllClientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Client
    template_name = "all_clients.html"
    context_object_name = "clients"

    def get_queryset(self):
        queryset = cache.get('all_clients')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('all_clients', queryset, 60 * 15)
        return queryset

    def test_func(self):
        # Проверка, что пользователь является менеджером
        return self.request.user.is_staff
