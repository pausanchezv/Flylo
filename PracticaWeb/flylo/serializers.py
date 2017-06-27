# coding=utf-8

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Flight, Aircraft, Category, Airline


class FlightSerializer(serializers.HyperlinkedModelSerializer):
    """ Serialitzador de l'entitat Flight """

    # el preu del vol es computa en temps real segons un algorisme especialitzat
    price = serializers.SerializerMethodField('compute_price')

    # usuari creador del vol
    #owner = serializers.ReadOnlyField(source='owner.username')

    @staticmethod
    def compute_price(obj):
        """ Calcula el preu del vol en temps real """
        return Flight.compute_flight_price_algorithm(obj)

    class Meta:

        """ Classe meta de l'entitat Flight """
        model = Flight
        fields = ('url', 'id', 'flight_number', 'location_departure','location_arrival', 'airlines', 'aircraft', 'estimated_time_departure', 'estimated_time_arrival', 'price')


class AircraftSerializer(serializers.HyperlinkedModelSerializer):
    """ Serialitzador de l'entitat Aircraft """

    # calcula el nombre de passatger de l'avió segons quants ocupants poden anar en cada categoria
    number_of_passengers = serializers.SerializerMethodField('compute_passengers_number')

    @staticmethod
    def compute_passengers_number(obj):
        """ Calcula el nombre de passatgers d'un avió """
        return Aircraft.get_total_aircraft_passengers(obj.category_set.all())

    class Meta:

        """ Classe meta de l'entitat Aircraft """
        model = Aircraft
        fields = ('url', 'id', 'name', 'first_flight_date', 'maximum_speed', 'number_of_passengers')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """ Serialitzador de l'entitat Category """

    class Meta:
        """ Classe meta de l'entitat Category """

        model = Category
        fields = ('url', 'id', 'name', 'aircraft', 'number_of_passengers')


class AirlineSerializer(serializers.HyperlinkedModelSerializer):
    """ Serialitzador de l'entitat Airline """

    # vols en què participa l'aerolinia
    flights_of_airline = serializers.SerializerMethodField()

    @staticmethod
    def get_flights_of_airline(obj):
        """ Obté els vols en què participa l'aerolinia """

        # es crea un diccionari de vols
        flights = {}

        for flight in obj.flight_set.all():

            # cada ID serà un akey pel diccionari de vols
            flights[flight.id] = {}

            # només es vol mostrar el número de vol
            flights[flight.id]['flight_number'] = flight.flight_number

        return flights

    class Meta:
        """ Classe meta de l'entitat Flight """

        model = Airline
        fields = ('url', 'id', 'name', 'long_name', 'country', 'telephone', 'year_foundation', 'flights_of_airline')


class UserSerializer(serializers.ModelSerializer):
    """ Serialitzador de l'entitat User de Django """

    flights = serializers.PrimaryKeyRelatedField(many=True, queryset=Flight.objects.all())

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'flights')
