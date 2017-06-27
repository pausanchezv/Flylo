# coding=utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Aircraft
from .models import Airline
from .models import Category
from .models import Client
from .models import Flight, ClientFlights

'''
Sobreescrivint l'admin per tenir en compte els objectes relacionats tal i com suggeriex el primer apartat
del tercer HomeWork.

FUNCIONAMENT:

Per crear le relacions de la base de dades s'han respectat de manera òptima les regles de formes normals del disseny de bases
de dades per tal de minimitzar les relacions evintant aquelles que són innecessaries.

Quan un usuari amb permisos es disposi a crear un avió, tindrà la opció d'afegir les categories que van lligades
a aquell avió que seran per tant les categories que l'avió ofereix als passatgers. I això és així degut a que
la relació és (un a molts).

Quan un usuari amb permisos es disposi a crear un vol, aquest serà l'encarregat de lligar al vol, l'avió i les
aerolinies amb les que treballa aquell vol.

El lligam entre avió i aerolinia és era una relació innecessaria tenint en compte un diseny òptim ja que les aerolinies
que treballen amb un avió poden ser accedides a partir dels vols que realitza aquell avió.

'''


class FlightAdmin(admin.ModelAdmin):
    """ Representació personalitzada de la llista de vols a l'admin """

    list_display = ('flight_number', 'location_departure', 'location_arrival', 'distance')


class CategoryInline(admin.StackedInline):
    """
    Representa les categories que té un avió
    Extra s'inicia a 0 perquè d'entrada només es pretén mostrar les categories que té el vol deixant-les modificar o
    afegir-ne més en cas que sigui necessari
    """
    model = Category
    extra = 1


class AircraftAdmin(admin.ModelAdmin):
    """ S'afegeixen els vols inline relacionats a cada avió """
    inlines = [CategoryInline]


class UserInline(admin.StackedInline):
    """ Es personalitzen els usuaris del sistema mitjançant extensions """
    model = Client
    can_delete = False
    verbose_name_plural = 'client'


class UserAdmin(BaseUserAdmin):
    """ Defineix un nou usuari """
    inlines = (UserInline, )


'''
Es fan visibles les taules a l'admin
'''

admin.site.register(Airline)
admin.site.register(Category)
admin.site.register(ClientFlights)

admin.site.register(Flight, FlightAdmin)
admin.site.register(Aircraft, AircraftAdmin)

# Registra de nou l'admin creat
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


