from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^edit/(?P<user_id>\d+)$', views.edit),
    url(r'^edit_user$', views.edit_user),
    url(r'^quotes$', views.quotes),
    url(r'^user_quotes/(?P<user_id>\d+)$', views.user_quotes),
    url(r'^quotes/(?P<quote_id>\d+)$', views.quotes_id),
    url(r'^quotes/ad$', views.quotes_ad),
    url(r'^quotes/(?P<quote_id>\d+)/update$', views.quotes_id_update),
    url(r'^favorite/(?P<quote_id>\d+)$', views.favorite),
    url(r'^unfavorite/(?P<quote_id>\d+)$', views.unfavorite),
    url(r'^quotes/(?P<quote_id>\d+)/destroy$', views.destroy),
    url(r'^quotes/(?P<quote_id>\d+)/edit$', views.quotes_id_edit),
]