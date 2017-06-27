# coding=utf-8

from django.core.urlresolvers import resolve

from flylo.models import Flight


class Settings(object):
    """ Classe que conté funcions i eines per gestionar el website """

    # nom del website
    SITE_NAME = 'FlyLo'

    # 1 any en segons
    YEAR_TIME = 365 * 24 * 60 * 60

    # límits
    URL_LIMIT_FROM = 7
    ID_LIMIT = 6

    # idioma del site per defecte
    DEFAULT_SITE_LANGUAGE = 'ca'

    @staticmethod
    def get_current_page(request):
        """ Retorna el nom de la pàgina html actual """
        return resolve(request.path_info).url_name

    @staticmethod
    def get_page_info(request, language):
        """ Retorna la informació bàsica de la pàgina actual"""

        current_page = Settings.get_current_page(request)
        constants_language = Settings.get_constants_language(language)

        info = {
            'request': request,
            'current_page': current_page,
            'current_path': request.get_full_path(),
            'meta': Settings.meta(constants_language, current_page),
            'current_language': language
        }

        # s'afegeixen les constants d'idiomes a la info de la pàgina
        info.update(constants_language)

        return info

    @staticmethod
    def redirect_to(page_info, cookie_language='ca'):
        """ Retorna el path per redirigir després d'afegir el llenguatge de la cookie"""

        path = page_info['current_path']
        first_path = path[:Settings.URL_LIMIT_FROM]
        second_path = path[Settings.URL_LIMIT_FROM:]

        return first_path + cookie_language + '/' + second_path

    @staticmethod
    def set_cookie_language(response, language):
        """ Afegeix la cookie de l'idioma favorit """
        response.set_cookie('language', language, Settings.YEAR_TIME)

    @staticmethod
    def add_language_from_cookie(request, language):
        """
        Estableix un llenguatge si no s'ha definit  prèviament seleccionant el català
        com a idioma per defecte. Si no, es retorna l'idioma preferit de l'usuari a través
        de la cookie del llenguatge
        """
        redirection = False

        if language == '':
            redirection = True

            if request.COOKIES.get('language'):
                language = request.COOKIES.get('language')
            else:
                language = 'ca'
        return language, redirection

    @staticmethod
    def meta(constants_language, current_page=None):
        """ Genera la meta-informació de cada pàgina del website"""

        # es generen els valors per defecte
        meta = {
            'title': Settings.SITE_NAME,
            'description': "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_SLOGAN']),
            'keywords': "vols, airplane, avió, flight",
            'author': constants_language['LANG_AUTHORS_NAME']
        }

        # es modifiquen les etiquetes segons la pàgina actual
        if current_page == 'flight-info':
            meta['title'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_FLIGHT_DETAILS'])
            meta['description'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_FLIGHT_DETAILS'])

        if current_page == 'flights':
            meta['title'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_FLIGHT_LIST'])
            meta['description'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_FLIGHT_LIST'])

        if current_page == 'airline-info':
            meta['title'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_AIRLINE_INFO'])
            meta['description'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_AIRLINE_INFO'])

        if current_page == 'aircraft-info':
            meta['title'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_AIRCRAFT_INFO'])
            meta['description'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_AIRCRAFT_INFO'])

        if current_page == 'buy':
            meta['title'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_SHOPPING_CART'])
            meta['description'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_SHOPPING_CART'])

        if current_page == 'buy-success':
            meta['title'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_BUY_SUCCESS_META'])
            meta['description'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_BUY_SUCCESS_META'])

        if current_page == 'checkin':
            meta['title'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_CHECKIN_META'])
            meta['description'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_CHECKIN_META'])

        if current_page == 'checkin-success':
            meta['title'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_CHECK_IN_SUCCESS_META'])
            meta['description'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_CHECK_IN_SUCCESS_META'])

        if current_page == 'login':
            meta['title'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_LOGIN'])
            meta['description'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_LOGIN'])

        if current_page == 'register':
            meta['title'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_REGISTER'])
            meta['description'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_REGISTER'])

        if current_page == 'userhome':
            meta['title'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_USERHOME'])
            meta['description'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_USERHOME'])

        if current_page == 'transaction-error':
            meta['title'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_TRANSACTION_ERROR_META'])
            meta['description'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_TRANSACTION_ERROR_META'])

        if current_page == 'comparator':
            meta['title'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_FLIGHT_COMPARATOR'])
            meta['description'] = "{} - {}".format(Settings.SITE_NAME, constants_language['LANG_FLIGHT_COMPARATOR'])

        return meta

    @staticmethod
    def get_constants_language(cookie_language=''):
        """ Assigna les constants d'idioma de la web """

        # es crea un prefix per distingir les constants d'idiomes als templates html
        lang_prefix = "LANG_"

        if cookie_language == 'ca' or cookie_language == '':
            from flylo.language.lang_ca import Language
            lang_ca = Language.get_language()
            return {lang_prefix + key: lang_ca[key] for key in lang_ca.keys()}

        if cookie_language == 'en':
            from flylo.language.lang_en import Language
            lang_en = Language.get_language()
            return {lang_prefix + key: lang_en[key] for key in lang_en.keys()}

    @staticmethod
    def fill_shopping_cart(shopping_cart, flight, flight_instance, post):
        """ Omple el carret de la compra """

        shopping_cart.cart[post[flight]]['obj'] = flight_instance
        shopping_cart.cart[post[flight]]['seats'] = post['seats_' + post[flight]]
        shopping_cart.cart[post[flight]]['airline'] = post['airline_' + post[flight]]
        shopping_cart.cart[post[flight]]['category'] = post['category_' + post[flight]]
        shopping_cart.cart[post[flight]]['return'] = None
        shopping_cart.cart[post[flight]]['price'] = flight_instance.price

        shopping_cart.inr_price(flight_instance.price * float(post['seats_' + post[flight]]))

    @staticmethod
    def fill_shopping_cart_returning(shopping_cart, flight, flight_return, post):
        """ Omple el carret de la compra pel vol de retorn, si n'hi ha"""

        flight_return.seats = post['seats_' + post[flight]]
        flight_return.airline = post['airline_return_' + post[flight]]
        flight_return.category = post['category_' + post[flight]]
        flight_return.price = Flight.compute_flight_price_algorithm(flight_return)
        shopping_cart.cart[post[flight]]['return'] = flight_return
        shopping_cart.inr_price(flight_return.price * float(post['seats_' + post[flight]]))

    @staticmethod
    def clean_variables_of_current_session(request):
        """ Neteja les variables de sessió """

        request.session["shopping_cart"] = ''

    @staticmethod
    def extract_int(string, char):
        """ Extreu l'enter final a partir d'un símbol """

        return string[char:]

    @classmethod
    def get_passengers_from_post(cls, request):
        """ Obté el nom delspassatgers d'un vol """

        # s'obtenen els POST relacionats amb nom i cognom dels passatgers
        passenger_names = filter(lambda x: x.startswith("passenger_name_"), request.POST)
        passenger_surnames = filter(lambda x: x.startswith("passenger_surname_"), request.POST)

        # s'extreu el valor d'aquests posts (nom i cognoms)
        passenger_names = map(lambda x: request.POST[x], passenger_names)
        passenger_surnames = map(lambda x: request.POST[x], passenger_surnames)

        # es fa unió perpendicular dels strings per posar en correspondència cada nom amb cada cognom
        passenger_complete_names = zip(passenger_names, passenger_surnames)
        passenger_complete_names = map(lambda x: x[0] + ' ' + x[1], passenger_complete_names)

        # s'inicialitza l'atribut com un string buit
        response= str()

        # s'omple l'atribut amb els noms dels passatgers per mostrar per pantalla
        for name in passenger_complete_names:
            response += name + '/'

        return response

    @classmethod
    def add_seats_to_flight(cls, request):
        """ Adjudica els seients als passatgers al fer checkIn """

        # s'obtenen els POST relacionats amb seients
        seats = filter(lambda x: x.startswith("passenger_seat_"), request.POST)

        # s'extreu el valor d'aquests seients
        seats = map(lambda x: request.POST[x], seats)

        string_seats = str()

        for seat in seats:
            string_seats += seat + '/'

        return string_seats









