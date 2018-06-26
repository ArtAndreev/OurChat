from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, \
    HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, RedirectView, \
    TemplateView

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
    context_object_name = 'messages'

    login_url = reverse_lazy('auth:login_view')

    queryset = model.objects.all().order_by('-id')


class MessagesView(LoginRequiredMixin, TemplateView):
    template_name = 'core/polling_messages.html'

    login_url = reverse_lazy('auth:login_view')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        last_id = self.request.GET.get('last_id')

        if last_id:
            messages = models.Message.objects.filter(id__gt=last_id).order_by('-id')[:20]
        else:
            messages = models.Message.objects.all().order_by('-id')
        data['messages'] = messages
        return data


class MessageCreateView(CreateView):
    form_class = forms.MessageCreateForm

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['post'])

    def get_success_url(self):
        return reverse('core:chat_view')

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({
            'renderedTemplate': render_to_string(
                'core/message.html',
                {
                    'message': self.object
                },
                self.request
            )
        })

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_invalid(self, form):
        return HttpResponseBadRequest()
