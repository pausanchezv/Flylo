# coding=utf-8
from django import template

register = template.Library()


@register.simple_tag
def get_at_index(array, index):
    """ Retorna un ítem d'un array segons el seu índex """
    return array[index]


@register.simple_tag
def get_index_from_value(array, value):
    """ Retorna l'índex d'un item en un array """
    return array.index(value)


@register.simple_tag
def get_num_seats_from_flight_id(session, flight_id):
    """ Retorna el nombre de seients reservats per un vol en una sessió """

    return session['shopping_cart'].cart[str(flight_id)]['seats']


@register.simple_tag
def get_airline_from_flight_id(session, flight_id):
    """ Retorna l'aerolinia per un vol en una sessió """

    return session['shopping_cart'].cart[str(flight_id)]['airline']


@register.simple_tag
def get_category_from_flight_id(session, flight_id):
    """ Retorna l'aerolinia per un vol en una sessió """

    return session['shopping_cart'].cart[str(flight_id)]['category']


@register.simple_tag
def get_return_from_flight_id(session, flight_id):
    """ Retorna l'aerolinia per un vol en una sessió """

    return session['shopping_cart'].cart[str(flight_id)]['return']


@register.simple_tag
def get_one():
    """ Retorna 1"""
    return '1'


@register.simple_tag
def get_true():
    """ Retorna true """
    return True


@register.simple_tag
def get_false():
    """ Retorna false"""
    return False


@register.simple_tag
def get_length(array):
    """ Retorna el tamany d'un array """
    return len(list(array))


@register.simple_tag
def get_price_of_shopping_cart(price_in, price_out):
    """ Retorna el preu del carret de la compra"""
    return price_in + price_out


@register.simple_tag
def get_string_for(length):
    """ Strings per recórrer templates """
    return int(length) * 'x'


@register.simple_tag
def get_integer_minus_one(integer):
    """ Retorna un enter -1 """
    return int(integer) - 1
