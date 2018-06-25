from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexPageView.as_view(), name='index_view'),
    url(r'^chat/$', views.ChatView.as_view(), name='chat_view'),
    url(r'^send/$', views.MessageCreateView.as_view(), name='send_view'),
]
