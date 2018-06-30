from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import View

from . import forms, models

# Create your views here.


class ChatLoginView(LoginView):
    template_name = 'authentication/signin.html'
    authentication_form = forms.LoginForm

    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('core:chat_view')


class ChatLogoutView(LogoutView):
    def get_next_page(self):
        return reverse('core:index_view')


class SignUpView(CreateView):
    template_name = 'authentication/signup.html'
    form_class = forms.SignUpForm

    success_url = reverse_lazy('auth:login_view')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('core:chat_view'))

        return super().get(request, *args, **kwargs)


class UserInfoView(View):
    http_method_names = ['get', ]

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return JsonResponse({
                'username': request.user.username,
                'avatar': request.user.avatar.url
            })

        else:
            return HttpResponse('Unauthorized', status=401)

