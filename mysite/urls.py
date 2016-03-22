"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth.views import login, password_change, logout
from django.conf.urls import url, include

from polls import views as vw
from cuser import views as vw_cuser


urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', vw.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', vw.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', vw.ResultsView.as_view(), name='results'),
    url(r'^admin/', admin.site.urls),
    url(r'^registration/$', vw_cuser.EmailUserRegistrationView.as_view(), name='registration'),
    url(r'^confirm-email/(?P<pk>\d+)/(?P<sign_user>[\w.@+-_]+)/', vw_cuser.EmailUserConfirmView.as_view(), name='confirm'),
    url(r'^login/$', login, {'template_name': 'cuser/login.html'}),
    url(r'^password_change/$', password_change, {'template_name': 'cuser/password_change.html', 'post_change_redirect': 'index'}),
    url(r'^logout/$', logout, {'next_page': 'index'}),
]
"""
 url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'cuser/login.html'}),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'cuser/password_change.html', 'post_change_redirect': 'index'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'index'}),
"""
