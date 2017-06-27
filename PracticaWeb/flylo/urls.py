# coding=utf-8
from django.conf.urls import url

from . import views

'''
Es defineixen els enllaços URL del website. Cal tenir encompte que com que es treballa amb diferents
llenguatges i es volen mostrar per URL cal considerar dues URL per cada cas (amb llenguatge i sense).
En cas d'executar una URL sense llenguatge, el sistema serà prou intel·ligent per detectar l'idioma
favorit de l'usuari i adjuntar el llenguatge a la URL.
'''

urlpatterns = [

    url(r'^(?P<language>[a-z]{2})/$', views.index, name='index'),
    url(r'^$', views.index, name='index'),

    url(r'^(?P<language>[a-z]{2})/shopping-cart/$', views.shopping_cart, name='shopping-cart'),
    url(r'^(?P<language>[a-z]{2})/buy/success/$', views.buy_success, name='buy-success'),
    url(r'^buy/success/$', views.buy_success, name='buy-success'),
    url(r'^(?P<language>[a-z]{2})/buy/$', views.buy, name='buy'),
    url(r'^buy/$', views.buy, name='buy'),

    url(r'^(?P<language>[a-z]{2})/buying/$', views.buying, name='buying'),
    url(r'^buying/$', views.buying, name='buying'),

    url(r'^(?P<language>[a-z]{2})/flights/$', views.flights, name='flights'),
    url(r'^flights/$', views.flights, name='flights'),

    url(r'^(?P<language>[a-z]{2})/flights/(?P<departure>.*)/$', views.flights, name='flights'),
    url(r'^flights/(?P<departure>.*)/$', views.flights, name='flights'),

    url(r'^(?P<language>[a-z]{2})/flight/(?P<flight_number>.*)/airline/(?P<name>.*)/info/$', views.airline_info, name='airline-info'),
    url(r'^flight/(?P<flight_number>.*)/airline/(?P<name>.*)/info/$', views.airline_info, name='airline-info'),

    url(r'^(?P<language>[a-z]{2})/flight/(?P<flight_number>.*)/info/$', views.flight_info, name='flight-info'),
    url(r'^flight/(?P<flight_number>.*)/info/$', views.flight_info, name='flight-info'),

    url(r'^(?P<language>[a-z]{2})/aircraft/(?P<name>.*)/info/$', views.aircraft_info, name='aircraft-info'),
    url(r'^aircraft/(?P<name>.*)/info/$', views.aircraft_info, name='aircraft-info'),

    url(r'^(?P<language>[a-z]{2})/flight/(?P<flight_number>.*)/checkin/success/$', views.do_checkin, name='checkin-success'),
    url(r'^flight/(?P<flight_number>.*)/checkin/success/$', views.do_checkin, name='checkin-success'),

    url(r'^(?P<language>[a-z]{2})/flight/(?P<flight_number>.*)/checkin/(?P<seats>.*)/$', views.checkin, name='checkin'),
    url(r'^flight/(?P<flight_number>.*)/checkin/(?P<seats>.*)/$', views.checkin, name='checkin'),

    url(r'^(?P<language>[a-z]{2})/users/login/$', views.login, name='login'),
    url(r'^users/login$', views.login, name='login'),

    url(r'^(?P<language>[a-z]{2})/users/register/$', views.register, name='register'),
    url(r'^users/register', views.register, name='register'),

    url(r'^(?P<language>[a-z]{2})/users/me/$', views.userhome, name='userhome'),
    url(r'^users/me', views.userhome, name='userhome'),

    url(r'^(?P<language>[a-z]{2})/users/logout/$', views.logout, name='logout'),
    url(r'^users/logout', views.logout, name='logout'),

    url(r'^(?P<language>[a-z]{2})/errors/transaction/$', views.transaction_error, name='transaction-error'),
    url(r'^errors/transaction', views.transaction_error, name='transaction-error'),

    url(r'^(?P<language>[a-z]{2})/comparator/$', views.comparator, name='comparator'),
    url(r'^comparator/$', views.comparator, name='comparator'),

    url(r'^remove-flight/(?P<flight_id>.*)/$', views.remove_flight_from_cart, name='remove-flight-from-cart'),
    url(r'^get-free/(?P<flight_number>.*)/$', views.get_free, name='get-free'),
]
