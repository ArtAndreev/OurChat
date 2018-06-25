from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.ChatLoginView.as_view(), name='login_view'),
    url(r'^logout/$', views.ChatLogoutView.as_view(), name='logout'),
    url(r'^signup/$', views.SignUpView.as_view(), name='signup_view'),
]
