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


class MessagesView(LoginRequiredMixin, View):
    login_url = reverse_lazy('auth:login_view')

    def get(self, request, *args, **kwargs):
        try:
            last_id = int(request.GET.get('last_id'))
        except TypeError:
            return HttpResponseBadRequest()
        except ValueError:
            return HttpResponseBadRequest()

        if last_id:
            messages = list(models.Message.objects.filter(
                id__gt=last_id).order_by('id')[:20])
        else:
            messages = list(models.Message.objects.all().order_by('id'))

        messages_list = []
        for message in messages:
            attaches = message.attachment_set.filter()
            attaches_list = []
            for attach in attaches:
                attaches_list.append({
                    'url': attach.file.url,
                    'filename': attach.filename,
                    'content_type': attach.content_type
                })

            messages_list.append({
                'id': message.id,
                'text': message.text,
                'date': message.date,
                'username': message.author.username,
                'avatar': message.author.avatar.url,
                'attaches': attaches_list
            })

        return JsonResponse({
            'messages': messages_list
        })


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
