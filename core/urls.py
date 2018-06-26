from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexPageView.as_view(), name='index_view'),
    url(r'^chat/$', views.ChatView.as_view(), name='chat_view'),
    url(r'^message/send/$',
        views.MessageCreateView.as_view(), name='send_view'),
    url(r'^message/get$', views.MessagesView.as_view(), name='get_view'),
]
