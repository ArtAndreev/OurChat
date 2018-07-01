from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, \
    HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, FormView
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


class MessageCreateView(FormView):
    form_class = forms.MessageCreateForm
    http_method_names = ['post', ]
    template_name = 'core/message.html'  # we don't really use it

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            message, attachments = form.save()
            if not attachments:
                return JsonResponse({
                    'id': message.id,
                    'text': message.text,
                    'date': message.date
                })
            else:
                return JsonResponse({
                    'id': message.id,
                    'text': message.text,
                    'date': message.date,
                    'attaches': attachments
                })
        else:
            return HttpResponseBadRequest()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
