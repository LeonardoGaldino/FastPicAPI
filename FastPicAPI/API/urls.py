"""FastPicAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from API import views

urlpatterns = [
    url(r'^onlineUsers/$', views.v_get_online_users),
    url(r'^rank/$', views.v_get_rank),
    url(r'^uploadImg/$', views.v_upload_image),
    url(r'^enterRoom/$', views.v_enter_room),
    url(r'^leaveRoom/$', views.v_leave_room),
    #url(r'create-room/$', views.create_room),
]
