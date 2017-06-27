# coding=utf-8
import os
from sqlite3 import IntegrityError

from django.contrib import auth
from django.contrib.auth.models import User
from django.db import transaction
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets

from flylo import permissions
from flylo.models import Flight, Aircraft, Airline, ShoppingCart, ClientFlights, Client, Category
from flylo.settings import Settings
from .serializers import FlightSerializer, AircraftSerializer, CategorySerializer, AirlineSerializer, UserSerializer


#########################################
########### Vistes de la WEB ############
#########################################


@require_http_methods(["GET", "POST"])
def login(request, language=''):
    """ Gestiona la pàgina de login al sistema """

    # es redirigeix a l'usuari al seu userhome si ja està logat
    if request.user.is_authenticated():
        return redirect("/flylo/" + language + "/users/me")

    # informació bàsica de la pàgina actual
    page_info = Settings.get_page_info(request, language)

    # s'afegeix l'idioma si la URL no el porta
    if language == '':
        cookie_language = request.COOKIES.get('language') if request.COOKIES.get('language') else Settings.DEFAULT_SITE_LANGUAGE
        return redirect(Settings.redirect_to(page_info, cookie_language))

    context = {
        'request': request
    }

    # es mira si s'arriba per POST, si és així vol dir que s'ha omplert el formulari
    # d'inici de sessió
    if request.method == 'POST' and request.POST['in-login'] == '1':

        # es reben els camps d'autentificació
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # s'autentifica l'usuari
        user = auth.authenticate(username=username, password=password)

        # es comprova que els camps de text hagin estat omplerts adientment
        if username.strip() and password.strip():

            # es mira que l'usuari estigui actiu al sistema
            if user is not None and user.is_active:

                # es loga l'usuari al sistema i es redirigeix a la seva pàgina privada
                auth.login(request, user)

                # es comprova si el motiu del login és un intent de compra i si és així enlloc de redirigir
                # a l'userhome fem que l'usuari torni a la pantalla del carret de compra disposat a executar
                # la compra dels vols
                if 'redirect_because_user_not_logged_in' in request.session.keys():

                    # es neteja la variable de sessió de redirecció i es redirigeix allà on toca
                    request.session['redirect_because_user_not_logged_in'] = ''
                    return HttpResponseRedirect("/flylo/" + language + "/buy")

                return HttpResponseRedirect("/flylo/" + language + "/users/me")

            else:
                context['error_message'] = page_info['LANG_USER_NOT_EXISTS']

        else:
            context['error_message'] = page_info['LANG_ALL_FILEDS_ARE_REQUIRED']

    # s'afegeix la infomació de la pàgina al context
    context.update(page_info)

    # es genera la resposta del servidor amb la sol·licitud la pàgina destí i el context
    response = render(request, 'flylo/login.html', context)

    # es crea la cookie de l'idioma si cal
    Settings.set_cookie_language(response, language)

    return response


@require_http_methods(["GET", "POST"])
def register(request, language=''):
    """ Registra un usuari en el sistema """

    # es redirigeix a l'usuari al seu userhome si ja està logat
    if request.user.is_authenticated():
        return redirect("/flylo/" + language + "/users/me")

    # informació bàsica de la pàgina actual
    page_info = Settings.get_page_info(request, language)

    # s'afegeix l'idioma si la URL no el porta
    if language == '':
        cookie_language = request.COOKIES.get('language') if request.COOKIES.get('language') else Settings.DEFAULT_SITE_LANGUAGE
        return redirect(Settings.redirect_to(page_info, cookie_language))

    context = {
        'request': request
    }

    # es mira si s'arriba per POST, si és així vol dir que s'ha omplert el formulari
    # de registre
    if request.method == 'POST' and request.POST['in-register'] == '1':

        # es reben els camps d'autentificació
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')

        # es comprova que tots els camps tinguin valor
        if username.strip() and password.strip() and email.strip():

            # no es permetrà repetir nom d'usuari
            try:
                User.objects.get(username=username)
                context['error_message'] = page_info['LANG_USER_EXISTS']

            # si l'usuari no existeix es procedeix al seu registre, es loga i finalment es redirigeix
            # a la seva pàgina privada d'usuari.
            except User.DoesNotExist:

                # es crea l'usuari
                user = User.objects.create_user(username, email, password)
                user.save()

                # se li afegeix rol de client i s'inicia el client amb mil euros
                client = Client(user=user, money=1000.0)
                client.save()

                # s'autologueja al registrar-se
                auth.login(request, user)

                # es comprova si el motiu del registre és un intent de compra i si és així enlloc de redirigir
                # a l'userhome fem que l'usuari torni a la pantalla del carret de compra disposat a executar
                # la compra dels vols
                if 'redirect_because_user_not_logged_in' in request.session.keys():

                    # es neteja la variable de sessió de redirecció i es redirigeix allà on toca
                    request.session['redirect_because_user_not_logged_in'] = ''
                    return HttpResponseRedirect("/flylo/" + language + "/buy")

                return HttpResponseRedirect("/flylo/" + language + "/users/me")

        else:
            context['error_message'] = page_info['LANG_ALL_FILEDS_ARE_REQUIRED']

    # s'afegeix la infomació de la pàgina al context
    context.update(page_info)

    # es genera la resposta del servidor amb la sol·licitud la pàgina destí i el context
    response = render(request, 'flylo/register.html', context)

    # es crea la cookie de l'idioma si cal
    Settings.set_cookie_language(response, language)

    return response


@require_http_methods("GET")
def logout(request, language=''):
    """ Tanca la sessió d'usuari i redirecciona a login """

    auth.logout(request)
    return HttpResponseRedirect("/flylo/" + language + "/users/login")


@require_http_methods(["GET", "POST"])
def userhome(request, language=''):
    """
    Representa la vista de la pàgina privada d'usuari
    Des d'aquesta vista serà possible realitzar els CheckIn dels vols adquirits
    """

    # per accedir a aquesta és condició impresicindible estar autenticat
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/flylo/" + language + "/users/login")

    # informació bàsica de la pàgina actual
    page_info = Settings.get_page_info(request, language)

    # s'afegeix l'idioma si la URL no el porta
    if language == '':
        cookie_language = request.COOKIES.get('language') if request.COOKIES.get('language') else Settings.DEFAULT_SITE_LANGUAGE
        return redirect(Settings.redirect_to(page_info, cookie_language))

    client_flights_items = ClientFlights.objects.filter(username=request.user.username)
    client_flights = []

    # s'obtenen els atributs que falten de la relació 'Flight' original.
    for flight in client_flights_items:
        flight_obj = Flight.objects.get(flight_number=flight.flight_number)
        flight_obj.airline = flight.airline
        flight_obj.seats = flight.seats
        flight_obj.category = flight.category
        flight_obj.status = flight.status
        flight_obj.passengers_names = flight.passengers_names.split('/')
        client_flights.append(flight_obj)

        # s'adapta el preu en funció de l'algorisme de càlcul de preu de vol
        flight_obj.price = Flight.compute_flight_price_algorithm(flight_obj)

    context = {
        'request': request,
        'client_flights': client_flights
    }

    # s'intenta accedir al client i es gestiona si es tracta de l'admin
    # normalment l'admin ppodria actuar com a client. Això és, però, una mesura de seguretat.
    try:
        user = User.objects.get(username=request.user.username)
        client = Client.objects.get(user=user)
        context['client'] = client

    except Client.DoesNotExist:
        context['error_client'] = True

    # s'afegeix la infomació de la pàgina al context
    context.update(page_info)

    # es genera la resposta del servidor amb la sol·licitud la pàgina destí i el context
    response = render(request, 'flylo/userhome.html', context)

    # es crea la cookie de l'idioma si cal
    Settings.set_cookie_language(response, language)

    return response


@require_http_methods("GET")
def index(request, language=''):
    """ Gestiona el template 'index.html' """

    # informació bàsica de la pàgina
    page_info = Settings.get_page_info(request, language)

    # s'assigna l'idioma de la pàgina (cookie/default)
    language, redirection = Settings.add_language_from_cookie(request, language)

    # es mira si cal redireccionar per afegir l'idioma de la cookie i es fa si escau
    if redirection:
        return redirect(page_info['current_path'] + language)

    # s'intenta fer la consulta requerida per paràmetre
    try:
        query = Flight.objects.values("location_departure").distinct()

    # si la consulta falla es redirecciona a 404
    except Flight.DoesNotExist:
        raise handler404(request)

    # es genera el context de la pàgina
    context = {
        'departures': query
    }

    # s'afegeix la infomació de la pàgina al context
    context.update(page_info)

    # es genera la resposta del servidor amb la sol·licitud la pàgina destí i el context
    response = render(request, 'flylo/index.html', context)

    # es crea la cookie de l'idioma si cal
    Settings.set_cookie_language(response, language)

    return response


@require_http_methods(["GET", "POST"])
def flights(request, language='', departure=''):
    """ Gestiona el template 'flights.html' """

    # informació bàsica de la pàgina actual
    page_info = Settings.get_page_info(request, language)

    # s'afegeix l'idioma si la URL no el porta
    if language == '':
        cookie_language = request.COOKIES.get('language') if request.COOKIES.get('language') else Settings.DEFAULT_SITE_LANGUAGE
        return redirect(Settings.redirect_to(page_info, cookie_language))

    # s'intenta fer la consulta requerida per paràmetre
    try:

        # es comprova que departure tingui valor per mostrar els vols requerits
        if departure != '':
            _flights = Flight.objects.filter(location_departure=departure)

        # en cas contrari es mostra tot el llistat de vols
        else:
            _flights = Flight.objects.all()
            departure = 'all'

    # si la consulta falla es redirecciona a 404
    except Flight.DoesNotExist:
        raise handler404(request)

    # es crea un diccionari que representa els vols de retorn per cada un dels vols
    return_flights = {}

    # per cada vol...
    for flight in _flights:

        # s'obtenen els seus vols de retorn
        return_flights[flight.id] = Flight.objects.filter(location_departure=flight.location_arrival, location_arrival=flight.location_departure)

        # s'adapta el preu en funció de l'algorisme de càlcul de preu de vol
        flight.price = Flight.compute_flight_price_algorithm(flight)

        # s'obtenen les quantitats de seients
        acquired_flights = ClientFlights.objects.filter(flight_number=flight.flight_number)
        number_of_seats_occupied = sum(af.seats for af in acquired_flights)
        number_of_seats_total = flight.aircraft.get_total_aircraft_passengers(flight.aircraft.category_set.all())

        # es crea un atribut del vol amb els seients disponibles
        flight.number_of_available_seats = number_of_seats_total - number_of_seats_occupied

    # vols de l'usuari de la sessió
    user_flights_ids = []

    # s'omple la llista de vols de l'usuari de la sessió per no oferir els mateixos vols més d'una vegada
    # en cas que l'usuari ja hagi adquirit el vol.
    if request.user.is_authenticated():
        user_flights = ClientFlights.objects.filter(username=request.user.username)

        for x in user_flights:
            user_flights_ids.append(x.flight_number)

    context = {
        'flights': _flights,
        'user_flights_ids': user_flights_ids,
        'return_flights': return_flights,
        'departure': departure
    }

    # s'afegeix la infomació de la pàgina al context
    context.update(page_info)

    response = render(request, 'flylo/flights.html', context)

    # es crea la cookie de l'idioma si cal
    Settings.set_cookie_language(response, language)

    return response


@require_http_methods("GET")
def flight_info(request, language='', flight_number=None):
    """ Gestiona el template 'flight-info.html' """

    # informació bàsica de la pàgina actual
    page_info = Settings.get_page_info(request, language)

    # s'afegeix l'idioma si la URL no el porta
    if language == '':
        cookie_language = request.COOKIES.get('language') if request.COOKIES.get('language') else Settings.DEFAULT_SITE_LANGUAGE
        return redirect(Settings.redirect_to(page_info, cookie_language))

    # s'intenta fer la consulta requerida per paràmetre
    try:
        flight = Flight.objects.get(flight_number=flight_number)

    # si la consulta falla es redirecciona a 404
    except Flight.DoesNotExist:
        raise handler404(request)

    # aerolinies que participen en el vol
    airlines = flight.airlines.all()

    # s'adapta el preu en funció de l'algorisme de càlcul de preu de vol
    flight.price = Flight.compute_flight_price_algorithm(flight)

    context = {
        'flight': flight,
        'airlines': airlines
    }

    # s'afegeix la infomació de la pàgina al context
    context.update(page_info)

    # es genera la resposta del servidor amb la sol·licitud la pàgina destí i el context
    response = render(request, 'flylo/flight-info.html', context)

    # es crea la cookie de l'idioma si cal
    Settings.set_cookie_language(response, language)

    return response


@require_http_methods("GET")
def aircraft_info(request, language='', name=''):
    """ Gestiona el template aircraft-info.html """

    # informació bàsica de la pàgina actual
    page_info = Settings.get_page_info(request, language)

    # s'afegeix l'idioma si la URL no el porta
    if language == '':
        cookie_language = request.COOKIES.get('language') if request.COOKIES.get('language') else Settings.DEFAULT_SITE_LANGUAGE
        return redirect(Settings.redirect_to(page_info, cookie_language))

    # s'intenta fer la consulta requerida per paràmetre
    try:
        aircraft = Aircraft.objects.get(name=name)

    # si la consulta falla es redirecciona a 404
    except Aircraft.DoesNotExist:
        raise Http404("Page not found")

    # Categories disponibles a l'avió
    aircraft_categories = aircraft.category_set.all()

    context = {
        'aircraft': aircraft,
        'aircraft_categories': aircraft_categories,
        'total_passengers': Aircraft.get_total_aircraft_passengers(aircraft_categories)
    }

    # s'afegeix la infomació de la pàgina al context
    context.update(page_info)

    # es genera la resposta del servidor amb la sol·licitud la pàgina destí i el context
    response = render(request, 'flylo/aircraft-info.html', context)

    # es crea la cookie de l'idioma si cal
    Settings.set_cookie_language(response, language)

    return response


@require_http_methods("GET")
def airline_info(request, language='', name='', flight_number=None):
    """ Gestiona el template airline-info.html """

    # informació bàsica de la pàgina actual
    page_info = Settings.get_page_info(request, language)

    # s'afegeix l'idioma si la URL no el porta
    if language == '':
        cookie_language = request.COOKIES.get('language') if request.COOKIES.get('language') else Settings.DEFAULT_SITE_LANGUAGE
        return redirect(Settings.redirect_to(page_info, cookie_language))

    # s'intenta fer la consulta requerida per paràmetre
    try:
        # aerolinia per la que es fa la query
        airline = Airline.objects.get(name=name)

        # vol pel qual es dóna informació sobre l'aerolinia
        flight = Flight.objects.get(flight_number=flight_number)

    # si la consulta falla es redirecciona a 404
    except Airline.DoesNotExist:
        raise handler404(request)

    # categories que ofereix l'aerolinia segons el vol
    airline_categories = flight.aircraft.category_set.all()

    context = {
        'flight': flight,
        'airline': airline,
        'airline_categories': airline_categories
    }

    # s'afegeix la infomació de la pàgina al context
    context.update(page_info)

    # es genera la resposta del servidor amb la sol·licitud la pàgina destí i el context
    response = render(request, 'flylo/airline-info.html', context)

    # es crea la cookie de l'idioma si cal
    Settings.set_cookie_language(response, language)

    return response


@require_http_methods("GET")
def buy(request, language=''):
    """
    Representa la vista de la pàgina del carret de compra. L'usuari està apunt de comprar.
    Aquesta vista no ha fer cap query de vols, doncs ha de mostrar les dades que persisteixen a la sessió.
    """

    # informació bàsica de la pàgina actual
    page_info = Settings.get_page_info(request, language)

    # s'afegeix l'idioma si la URL no el porta
    if language == '':
        cookie_language = request.COOKIES.get('language') if request.COOKIES.get('language') else Settings.DEFAULT_SITE_LANGUAGE
        return redirect(Settings.redirect_to(page_info, cookie_language))

    # es genera el cobtext del template
    context = {
        'request': request
    }

    # es comprova si hi ha sessió d'usuari tenint en compte que es pot arribar al carret de compra
    # amb sessió o sense. S' s'hi arriba amb sessió, s'haurà de comprovar que l'usuari té prous diners
    if request.user.is_authenticated():

        client = None

        # s'intenta accedir a l'usuari client
        try:

            user = User.objects.get(username=request.user.username)
            client = Client.objects.get(user=user)

            # es comprova si l'usuari té prous diners per comprar
            try:
                context['user_has_money_to_buy'] = client.money >= request.session["shopping_cart"].get_price()

            except AttributeError:
                context['user_has_money_to_buy'] = True

            context['current_client_money'] = client.money

        # si no el troba vol dir que s'ha accedit amb un compte d'admin. S'avisa de l'error.
        except Client.DoesNotExist:
            context['client_error'] = page_info['LANG_ERROR_USER_IS_NOT_A_CLIENT']

        # si el carret encara no té preu és que s'hi accedeix per capcelera. S'estableix la quantia de diners del client
        except KeyError:
            context['current_client_money'] = client.money
            context['user_has_money_to_buy'] = True

    # s'afegeix la infomació de la pàgina al context
    context.update(page_info)

    # es genera la resposta del servidor amb la sol·licitud la pàgina destí i el context
    response = render(request, 'flylo/shopping-cart.html', context)

    # es crea la cookie de l'idioma si cal
    Settings.set_cookie_language(response, language)

    return response


@transaction.atomic
@require_http_methods("GET")
def buying(request, language=''):
    """
    El client executa la compra dels vols que té al ShoppingCart
    Aquesta és una operació atòmica ja que dues o més persones no poden executar un compra
    si queden menys seients dels necessaris per satisfer a tothom.
    A l'informe s'explica amb tota mena de detall.
    """

    # es comprova si l'usuari que prem el botó de comprar està logat en el sistema
    if not request.user.is_authenticated():

        # es crea una variable de sessió per tornar aqui una vegada inicii la seva sessió
        request.session['redirect_because_user_not_logged_in'] = 'redirect_to_shopping_cart'
        return HttpResponseRedirect("/flylo/" + language + "/users/login")

    # tractament específic d'operació atòmica
    try:
        with transaction.atomic():

            # s'aconsegueixen tots els vols del carret de l'usuari a través de la sessió
            user_flight_list = list(request.session['shopping_cart'].cart.keys())

            # es construeixen els vols amb els identificadors i es creen les entitats ClientVol
            for flight_id in user_flight_list:

                flight = Flight.objects.get(pk=flight_id)

                seats = request.session['shopping_cart'].cart[str(flight_id)]['seats']
                airline = request.session['shopping_cart'].cart[str(flight_id)]['airline']
                category = request.session['shopping_cart'].cart[str(flight_id)]['category']

                client_flight = ClientFlights(username=request.user.username, flight_number=flight.flight_number, airline=airline, seats=seats, category=category)
                client_flight.save()

                if request.session['shopping_cart'].cart[str(flight_id)]['return']:

                    seats = request.session['shopping_cart'].cart[str(flight_id)]['return'].seats
                    airline = request.session['shopping_cart'].cart[str(flight_id)]['return'].airline
                    category = request.session['shopping_cart'].cart[str(flight_id)]['return'].category

                    client_flight = ClientFlights(username=request.user.username, flight_number=request.session['shopping_cart'].cart[str(flight_id)]['return'].flight_number, airline=airline, seats=seats, category=category)
                    client_flight.save()

            # S'obté l'usuari de la sessió (no necessita try/except perquè en aquest punt és imprescindible
            # arrribar-hi amb sessió de client
            user = User.objects.get(username=request.user.username)
            client = Client.objects.get(user=user)

            # es redueix el saldo el client en funció del preu de la compra
            client.money -= request.session["shopping_cart"].get_price()
            client.save()

            # s'alliberen les variables de sessió.
            # Ara ja tenim el client relacionat amb els seus vols adquirits
            Settings.clean_variables_of_current_session(request)

            return HttpResponseRedirect("/flylo/" + language + "/buy/success")

    # si l'update ha fallat es redirigeix a una pàgina personalitzada d'error
    except IntegrityError:
        return redirect('/flylo/' + language + '/errors/transaction')


@require_http_methods("POST")
def shopping_cart(request, language):
    """
    Crea la sessió pel carret de la compra.
    Aqui no es genera cap context, quan es rep el POST es crea la sessió amb la informació necessaria
    i es fa un redirect a la pàgina de compra, la qual arribarem per GET.
    """

    # es comença suposant que el carret de la compra encara no existeix
    shopping_cart = ShoppingCart(0.0)

    # es comprova que realment no existeix
    try:

        # en cas d'existir el carret de la compra es fa servir el ja existent per no machacar-lo
        if request.session["shopping_cart"] and request.session["shopping_cart"] != '':
            shopping_cart = request.session["shopping_cart"]
            shopping_cart.set_price(0.0)

    # en cas d'error de clau no cal actuar de cap manera, simplement es deixa seguir el fluxe de l'execució
    except KeyError:
        pass

    # es filtren les variables POST que representen vols
    _flights = filter(lambda x: x.startswith("flight_"), request.POST)

    # s'iteren els vols i se'ls afegeix la seva info de compra corresponent
    for flight in _flights:

        # s'obté l'objecte del vol
        flight_instance = Flight.objects.get(pk=request.POST[flight])

        # s'adapta el preu del vol en funció de l'algorisme de càlcul de preu de vol
        flight_instance.price = Flight.compute_flight_price_algorithm(flight_instance)

        # creació del diccionari de característiques del vol
        shopping_cart.cart[request.POST[flight]] = {}

        # s'omple el carret de la compra
        Settings.fill_shopping_cart(shopping_cart, flight, flight_instance, request.POST)

        # es mira si l'usuari ha triat vol de retorn i es té ne compte en tal cas
        if request.POST['returns_' + request.POST[flight]]:

            # s'obté el vol de retorn
            flight_return = Flight.objects.get(flight_number=str(request.POST['returns_' + request.POST[flight]][:Settings.ID_LIMIT]))

            # s'omplen les dades del vol de retorn
            Settings.fill_shopping_cart_returning(shopping_cart, flight, flight_return, request.POST)

        # s'adjunta el vol com a objecte particular del carret de la compra
        shopping_cart.add_flight_to_cart(request.POST[flight], flight_instance)

    # es crea la sessió i s'adjunta únicament l'objecte del model que representa el carret de la compra
    request.session["shopping_cart"] = shopping_cart

    # es retorna redirigint ja que venim per POST i es va a parar a la pàgina del carret per GET
    return HttpResponseRedirect(reverse('flylo:buy', args=(language,)))


@require_http_methods("GET")
def remove_flight_from_cart(request, flight_id):
    """
    Elimina un vol de la sessió directament des de la pàgina de vols.
    Aquest mètode permet eliminar un vol directament quan es fa click al checkbox per des-seleccionar
    un vol que havia estat prèviament seleccionat
    """

    # es comprova si existeix un carret de compra
    try:

        # es comprova si hi ha vols a la sessió
        if request.session['shopping_cart'] and request.session['shopping_cart'] != '':

            # es comprova si el carret conté el vol que es pretén eliminar
            if str(flight_id) in request.session['shopping_cart'].cart.keys():

                # es comprova si hi ha vol de retorn pel vol
                try:

                    # es comprova si tenia vol de retorn
                    if request.session['shopping_cart'].cart[str(flight_id)]['return']:

                        # es decrementa el valor del carret pel preu vol de retorn
                        request.session['shopping_cart'].dcr_price(request.session['shopping_cart'].cart[str(flight_id)]['return'].price * float(request.session['shopping_cart'].cart[str(flight_id)]['seats']))

                    # es decrementa el valor del carret pel preu vol
                    request.session['shopping_cart'].dcr_price(request.session['shopping_cart'].cart[str(flight_id)]['price'] * float(request.session['shopping_cart'].cart[str(flight_id)]['seats']))

                # si hi ha error simplement no es fa res
                except (KeyError, ValueError):
                    pass

                # s'elimina el vol del carret de la compra
                removed_cart = request.session['shopping_cart'].remove_flight_from_cart(str(flight_id))
                request.session['shopping_cart'] = removed_cart

    # si hi ha error simplement no es fa res
    except KeyError:
        pass

    return HttpResponse()


@require_http_methods("GET")
def checkin(request, language='', flight_number=None, seats=1):
    """ Gestions el template checkin.html on l'usuari executarà el checkin """

    # informació bàsica de la pàgina actual
    page_info = Settings.get_page_info(request, language)

    # s'afegeix l'idioma si la URL no el porta
    if language == '':
        cookie_language = request.COOKIES.get('language') if request.COOKIES.get('language') else Settings.DEFAULT_SITE_LANGUAGE
        return redirect(Settings.redirect_to(page_info, cookie_language))

    # s'intenta fer la consulta requerida per paràmetre
    try:
        flight = Flight.objects.get(flight_number=flight_number)

    # si la consulta falla es redirecciona a 404
    except Flight.DoesNotExist:
        raise handler404(request)

    # afegint rellevant info al vol
    flight.seats = seats
    flight.capacity = Aircraft.get_total_aircraft_passengers(flight.aircraft.category_set.all())

    context = {
        'request': request,
        'flight': flight
    }

    # s'afegeix la infomació de la pàgina al context
    context.update(page_info)

    # es crea la resposta del server
    response = render(request, 'flylo/checkin.html', context)

    # es crea la cookie de l'idioma si cal
    Settings.set_cookie_language(response, language)

    return response


@transaction.atomic
@require_http_methods(["GET", "POST"])
def do_checkin(request, language='', flight_number=None):
    """
    Executa el check-in. La funció es diu success ja que si arribem a aquest punt vol dir que
    s'acompleixen totes les condicions per fer efectiu el checkin.

    La primer vegada s'arriba per POST, s'executa el checkin i es redirigeix sobre ell mateix per GET,
    aleshores es mostra el missatge d'èxit a l'usuari.
    """
    # informació bàsica de la pàgina actual
    page_info = Settings.get_page_info(request, language)

    # s'afegeix l'idioma si la URL no el porta
    if language == '':
        cookie_language = request.COOKIES.get('language') if request.COOKIES.get('language') else Settings.DEFAULT_SITE_LANGUAGE
        return redirect(Settings.redirect_to(page_info, cookie_language))

    # si s'arriba per POST s'executa el check-in i ràpidament es redirigeix per GET
    if request.method == 'POST' and request.POST['in-checkin'] == '1':

        # s'obté el vol dels vols generals (per ocupar el seient pel passatger)
        flight = Flight.objects.get(flight_number=flight_number)

        # tractament específic d'operació atòmica
        try:
            with transaction.atomic():

                # s'ocupen els seients a l'avió
                # és molt important apreciar que si s'ha arribat a aquest punt vol dir que els seients estaven lliures
                # ja que s'han fet les comprovacions per Front-End a la funció de JavaScript del fitxer checkin.html,
                # però si una persona fa click abans que l'altra l'única manera possible d'asegurar la integritat
                # de l'operació és fent que sigui atòmica
                flight.seats_occupied += Settings.add_seats_to_flight(request)

                # s'executa l'update
                flight.save()

                # s'obté el vol dels vols del client
                client_flight = ClientFlights.objects.get(flight_number=flight_number, username=request.user.username)

                # s'obté el nom dels passatgers del vol
                client_flight.passengers_names = Settings.get_passengers_from_post(request)

                # es canvia l'estat del vol del client
                client_flight.status = 'after_checkin'

                # s'executa l'update
                client_flight.save()

        # si l'update ha fallat es redirigeix a una pàgina personalitzada d'error
        except IntegrityError:
            return redirect('/flylo/' + language + '/errors/transaction')

        return HttpResponseRedirect(page_info['current_path'])

    context = {
        'request': request,
        'flight_number': flight_number
    }

    # s'afegeix la infomació de la pàgina al context
    context.update(page_info)

    # es genera la resposta del servidor amb la sol·licitud la pàgina destí i el context
    response = render(request, 'flylo/checkin-success.html', context)

    # es crea la cookie de l'idioma si cal
    Settings.set_cookie_language(response, language)

    return response


@require_http_methods("GET")
def transaction_error(request, language=''):
    """ Gestiona els errors atòmics de transacció """

    # informació bàsica de la pàgina actual
    page_info = Settings.get_page_info(request, language)

    # s'afegeix l'idioma si la URL no el porta
    if language == '':
        cookie_language = request.COOKIES.get('language') if request.COOKIES.get('language') else Settings.DEFAULT_SITE_LANGUAGE
        return redirect(Settings.redirect_to(page_info, cookie_language))

    # es genera la resposta del servidor amb la sol·licitud la pàgina destí i el context
    response = render(request, 'flylo/transaction-error.html', page_info)

    # es crea la cookie de l'idioma si cal
    Settings.set_cookie_language(response, language)

    return response


@require_http_methods("GET")
def buy_success(request, language=''):
    """ Gestiona la compra realitzada """

    # informació bàsica de la pàgina actual
    page_info = Settings.get_page_info(request, language)

    # s'afegeix l'idioma si la URL no el porta
    if language == '':
        cookie_language = request.COOKIES.get('language') if request.COOKIES.get('language') else Settings.DEFAULT_SITE_LANGUAGE
        return redirect(Settings.redirect_to(page_info, cookie_language))

    # es genera la resposta del servidor amb la sol·licitud la pàgina destí i el context
    response = render(request, 'flylo/buy-success.html', page_info)

    # es crea la cookie de l'idioma si cal
    Settings.set_cookie_language(response, language)

    return response


@require_http_methods("GET")
def handler404(request):
    """ Gestiona l'error 404 """
    return Http404("Page not found")


@require_http_methods("GET")
def comparator(request, language=''):
    """ Gestiona el comparador de vols """

    # informació bàsica de la pàgina actual
    page_info = Settings.get_page_info(request, language)

    # s'afegeix l'idioma si la URL no el porta
    if language == '':
        cookie_language = request.COOKIES.get('language') if request.COOKIES.get('language') else Settings.DEFAULT_SITE_LANGUAGE
        return redirect(Settings.redirect_to(page_info, cookie_language))

    # llegeix les ips del fitxer de ips
    with open(os.path.join('flylo/static/flylo/files/', 'ip.dat')) as ip_reader:
        list_of_addresses = filter(lambda x: x != '\n', ip_reader)
        list_of_addresses = [line.rstrip() for line in list_of_addresses if line.endswith('\n')]

    # es genera el context de l'html
    context = {
        'list_of_addresses': list_of_addresses,
        'user_agent': request.META['HTTP_USER_AGENT'],
        'is_alert': 'firefox' in str(request.META['HTTP_USER_AGENT']).lower()
    }

    # s'adjunta la informació de pàgina al context
    context.update(page_info)

    # es genera la resposta del servidor amb la sol·licitud la pàgina destí i el context
    response = render(request, 'flylo/comparator.html', context)

    # es crea la cookie de l'idioma si cal
    Settings.set_cookie_language(response, language)

    print ('firefox' in str(request.META['HTTP_USER_AGENT']).lower())

    return response


@require_http_methods("GET")
def get_free(request, flight_number):
    """ Comprova els seients d'un vol que estan ocupats """

    # s'intenta fer la consulta requerida per paràmetre
    try:
        flight = Flight.objects.get(flight_number=flight_number)

    # si la consulta falla es redirecciona a 404
    except Flight.DoesNotExist:
        raise handler404(request)

    return HttpResponse(flight.seats_occupied)



#########################################
########### Vistes de la API ############
#########################################


class AircraftViewSet(viewsets.ModelViewSet):
    """
    API que permet editar o visualitzar els els avions
    """
    queryset = Aircraft.objects.all().order_by('name')
    serializer_class = AircraftSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API que permet editar o visualitzar les categories
    """
    queryset = Category.objects.all().order_by('aircraft')
    serializer_class = CategorySerializer


class AirlineViewSet(viewsets.ModelViewSet):
    """
    API que permet editar o visualitzar les aerolinies
    """
    queryset = Airline.objects.all().order_by('name')
    serializer_class = AirlineSerializer


class FlightViewSet(viewsets.ModelViewSet):
    """
    API que permet editar o visualitzar els vols
    """

    # per defecte s'ordenen les vistes per nombre de vol
    queryset = Flight.objects.all().order_by('flight_number')
    serializer_class = FlightSerializer

    def perform_create(self, serializer):
        """ Obté i serialitza el creador del vol per poder-lo modificar posteriorment """
        serializer.save(owner=self.request.user)

    # cal sobreescriure el queryset per poder utilitzar el comparador de vols
    def get_queryset(self):
        """
        Filtres per URL
        """
        queryset = Flight.objects.all()

        # s'obtenen els paràmetres GET
        departure = self.request.query_params.get('departure', '')
        arrival = self.request.query_params.get('arrival', '')
        departure_time = self.request.query_params.get('departure_time', '')
        arrival_time = self.request.query_params.get('arrival_time', '')

        # Es configuren totes les possibles combinacions de query possibles
        if departure != '' and arrival != '' and departure_time != '' and arrival_time != '':
            queryset = queryset.filter(location_departure=departure, location_arrival=arrival, estimated_time_departure=departure_time, estimated_time_arrival=arrival_time)

        if departure != '' and arrival != '' and departure_time != '':
            queryset = queryset.filter(location_departure=departure, location_arrival=arrival, estimated_time_departure=departure_time)

        if departure != '' and arrival != '' and arrival_time != '':
            queryset = queryset.filter(location_departure=departure, location_arrival=arrival, estimated_time_arrival=arrival_time)

        if departure != '' and departure_time != '' and arrival_time != '':
            queryset = queryset.filter(location_departure=departure, estimated_time_departure=departure_time, estimated_time_arrival=arrival_time)

        if arrival != '' and departure_time != '' and arrival_time != '':
            queryset = queryset.filter(location_arrival=arrival, estimated_time_departure=departure_time, estimated_time_arrival=arrival_time)

        if departure != '' and arrival != '':
            queryset = queryset.filter(location_departure=departure, location_arrival=arrival)

        if departure != '' and departure_time != '':
            queryset = queryset.filter(location_departure=departure, estimated_time_departure=departure_time)

        if departure != '' and arrival_time != '':
            queryset = queryset.filter(location_departure=departure, estimated_time_arrival=arrival_time)

        if arrival != '' and departure_time != '':
            queryset = queryset.filter(location_arrival=arrival, estimated_time_departure=departure_time)

        if arrival != '' and arrival_time != '':
            queryset = queryset.filter(location_arrival=arrival, estimated_time_arrival=arrival_time)

        if departure_time != '' and arrival_time != '':
            queryset = queryset.filter(estimated_time_departure=departure_time, estimated_time_arrival=arrival_time)

        elif departure != '':
            queryset = queryset.filter(location_departure=departure)

        elif arrival != '':
            queryset = queryset.filter(location_arrival=arrival)

        elif departure_time != '':
            queryset = queryset.filter(estimated_time_departure=departure_time)

        elif arrival_time != '':
            queryset = queryset.filter(estimated_time_arrival=arrival_time)

        return queryset

    # s'afegeixen els permisos d'usuari
    permission_classes = (permissions.IsComercialOrReadOnly, permissions.IsOwnerOrReadOnly, )


class UserList(viewsets.ReadOnlyModelViewSet):
    """ Api que gestiona els usuaris del website """
    queryset = User.objects.all()
    serializer_class = UserSerializer

