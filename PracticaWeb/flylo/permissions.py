# coding=utf-8
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Afegint permís de modificació únicament als autors dels vols
    """

    def has_object_permission(self, request, view, obj):
        """ Es comproven els permisos """

        if request.method in permissions.SAFE_METHODS:
            return True

        # Només si l'usuari comercial ha creat el vol el podrà editar o eliminar
        return obj.owner == request.user


class IsComercialOrReadOnly(permissions.BasePermission):
    """
    Afegint permisos de creació de vols únicament als administradors comercials
    """

    def has_permission(self, request, view):
        """ Es comproven els permisos """

        if request.method in permissions.SAFE_METHODS:
            return True

        # Només si l'usuari és un comercial podrà afegir vols
        return request.user.groups.filter(name="Comercial_to_add_flights").exists()
