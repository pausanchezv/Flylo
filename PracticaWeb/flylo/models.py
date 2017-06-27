# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Airline(models.Model):
    """ Representa una entitat Aerolínia """

    country = models.CharField('Country', max_length=8)
    name = models.CharField('Short Name', max_length=3)
    long_name = models.CharField('Long Name', max_length=20)
    telephone = models.CharField('Telephone number', max_length=9)
    year_foundation = models.CharField('Foundation year', max_length=4)

    def __str__(self):
        """ Representació de l'entitat en text """
        return "{} ({})".format(self.name, self.long_name)


class Aircraft(models.Model):
    """ Representa una entitat avió """

    name = models.CharField(max_length=4)

    construction_date = models.DateField('Construction date')
    first_flight_date = models.DateField('Date of first flight')
    maximum_speed = models.FloatField('Maximum speed (km/h)')

    def __str__(self):
        """ Representació de l'entitat en text """
        return self.name

    @staticmethod
    def get_total_aircraft_passengers(aircraft_categories):
        """
        Calcula el nombre de passatgers total d'un avió a partir del nombre
        de passatges de cadascuna de les seves categories
        """
        return sum(category.number_of_passengers for category in aircraft_categories)


class Flight(models.Model):
    """ Representa una entitat vol """

    flight_number = models.CharField('Flight number', max_length=8)
    estimated_time_departure = models.DateTimeField('Estimated departure')
    estimated_time_arrival = models.DateTimeField('Estimated arrival')
    location_departure = models.CharField('Location departure', max_length=3)
    location_arrival = models.CharField('Location arrival', max_length=3)
    status = models.CharField('Current state', max_length=40, default='DELAYED')
    distance = models.FloatField('Flight Distance (km)', default=400.0)
    seats_occupied = models.CharField('Seats occupied', max_length=1000, default='/')

    owner = models.ForeignKey('auth.User', related_name='flights', on_delete=models.CASCADE)

    # Relació >> un vol té associat un avió però un avió pot fer molts vols
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)

    # Relació >> moltes aerolinies participen en molts vols
    airlines = models.ManyToManyField(Airline)

    def __str__(self):
        """ Representació de l'entitat en text """
        return self.flight_number

    @staticmethod
    def compute_flight_price_algorithm(flight):
        """
        Calcula el preu d'un vol
        L'algorisme parteix d'un preu inicial calculat amb la distància del vol. Aquest preu s'anirà encarint
        a mesura que la data sortida del vol es vagi aproximant i en funció de quantes aerolinies participin en el vol.
        Si un vol és exclussiu d'una aerolinia serà més car que si és compartit entre diverses aerolinies.
        L'avió també juga un paper important en el càlcul del preu d'un vol: si un avió té menys capacitat es considera
        més íntim i luxós fent encarir el preu del vol
        """

        from datetime import datetime

        # Es calcula quants dies queden per la sortida del vol
        difference_days = (flight.estimated_time_departure.replace(tzinfo=None) - datetime.now()).days

        # Es computa el nombre d'aerolinies implicades en el vol
        implicated_airlines = len(list(flight.airlines.all()))

        # S'obtenen les categories implicades en el vol
        aircraft_categories = flight.aircraft.category_set.all()

        # Amb les categories es computa la capacitat total
        capacity = Aircraft.get_total_aircraft_passengers(aircraft_categories)

        # inicialment es a dependre el preu de la distància
        price = flight.distance * 0.3

        # Es descompta preu al vol com abans es compri (diferència temporal)
        price -= difference_days * 0.4

        # S'augmenta el preu d'un vol en funció de les aerolinies que hi participen (confiança)
        if implicated_airlines == 4:
            price += 0.0

        elif implicated_airlines == 3:
            price += 10.0

        elif implicated_airlines == 2:
            price += 20.0

        elif implicated_airlines == 1:
            price += 30.0

        # Es modifica el preu segons el nombre de passatgers de l'avió (intimitat)
        if capacity > 500:
            price += 0.0

        elif 500 > capacity > 300:
            price += 20

        else:
            price += 50

        # es retorna el preu adaptat de manera algorísmica
        return price


class Client(models.Model):
    """ Representa un usuari de la pàgina web """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.FloatField('User current money')

    def __str__(self):
        """ Representació de l'entitat en text """
        return self.user.username


class ClientFlights(models.Model):
    """ Entitat que relaciona un client amb els seus vols adquirits"""

    username = models.CharField('Username', max_length=20)
    flight_number = models.CharField('Flight number', max_length=8)
    airline = models.CharField('Airline', max_length=20, default='')
    seats = models.IntegerField('Number of seats', default=1)
    category = models.CharField('Flight category', max_length=20, default='economic')
    status = models.CharField('Flight status', max_length=20, default='before_checkin')
    passengers_names = models.TextField('Names of passengers', default='')

    def __str__(self):
        """ Representació de l'entitat en text """
        return "{} - {} - {} - {} - {}".format(self.username, self.flight_number, self.airline, self.category, self.status)


class Category(models.Model):
    """ Representa una entitat categoria """

    name = models.CharField('Category name', max_length=12)
    number_of_passengers = models.IntegerField('Number of passengers')

    # Relació >> un avió pot oferir diverses categories (economic, business, etc)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)

    def __str__(self):
        """ Representació de l'entitat en text """
        return "{} for aircraft: ({})".format(self.name, self.aircraft)


class ShoppingCart(object):
    """ Objecte del model per representar el carret de compra tal i com suggereix l'enunciat """

    def __init__(self, price):
        """ Inicialitza el carret """

        # diccionari que contindrà els vols del carret de la compra
        self.cart = {}

        # valor econòmic del carret de la compra
        self.price = price

    def get_price(self):
        """ Retorna el preu del carret """
        return self.price

    def set_price(self, price):
        """ Retorna el preu del carret """
        self.price = price

    def remove_flight_from_cart(self, flight):
        """ Elimina un vol del carret """
        del self.cart[flight]
        return self

    def add_flight_to_cart(self, flight, instance):
        """ Afegeix un vol al carret de la compra """
        self.cart[flight]['obj'] = instance

    def inr_price(self, price):
        """ Incrementa el preu del carret a l'afegir un nou vol """
        self.price += price

    def dcr_price(self, price):
        """ Decrementa el preu del carret al treure un vol """
        self.price -= price

    def __str__(self):
        """ Representació del Shpiing Cart com a string """
        return "Price: {}\nCart: {}".format(self.price, self.cart)












