from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, \
    HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, RedirectView

from . import forms, models

# Create your views here.


class IndexPageView(RedirectView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('core:chat_view'))
        else:
            return HttpResponseRedirect(reverse('auth:login_view'))


class ChatView(LoginRequiredMixin, ListView):
    model = models.Message
    template_name = 'core/chat.html'

    login_url = reverse_lazy('auth:login_view')

    queryset = models.Message.objects.all().order_by('-date')


class MessageCreateView(CreateView):
    form_class = forms.MessageCreateForm

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['post'])

    def get_success_url(self):
        return reverse('core:chat_view')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_invalid(self, form):
        return HttpResponseBadRequest()
