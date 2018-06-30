from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, \
    HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.base import View

from . import forms, models

# Create your views here.


class IndexPageView(View):
    http_method_names = ['get', ]

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('core:chat_view'))
        else:
            return HttpResponseRedirect(reverse('auth:login_view'))


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'core/chat.html'

    login_url = reverse_lazy('auth:login_view')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        user_id = kwargs.get('id')
        messages = models.Message.objects.all().order_by('-id')
        data['messages'] = messages
        # dialog_list = models.ChatDialog.objects.get_user_dialogs(user_id)
        # room_list = models.ChatRoom.objects.get_user_rooms(user_id)
        #
        # data['dialog_list'] = dialog_list
        # data['room_list'] = room_list
        return data


# class ChatDialogView(LoginRequiredMixin, ListView):
#     model = models.ChatDialog
#     template_name = 'core/chat.html'
#     context_object_name = 'messages'
#
#     login_url = reverse_lazy('auth:login_view')
#
#     queryset = model.objects.all().order_by('-id')


class MessagesView(LoginRequiredMixin, TemplateView):
    template_name = 'core/polling_messages.html'

    login_url = reverse_lazy('auth:login_view')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        last_id = self.request.GET.get('last_id')

        if last_id:
            messages = models.Message.objects.filter(
                id__gt=last_id).order_by('-id')[:20]
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
        response = JsonResponse({
            'id': self.object.id,
            'text': self.object.text,
            'date': self.object.date
        })

        return response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_invalid(self, form):
        return HttpResponseBadRequest()
