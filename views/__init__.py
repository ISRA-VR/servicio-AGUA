#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
PAQUETE VIEWS - CAPA DE VISTAS (MVC)
=============================================================================

Este paquete contiene todas las interfaces de usuario del sistema.

RESPONSABILIDAD DE LAS VIEWS:
- Mostrar información al usuario
- Capturar entrada del usuario
- Enviar acciones a los Controllers
- NO contienen lógica de negocio

ARCHIVOS DEL PAQUETE:
- auth_view.py: Pantalla de login/autenticación
- main_view.py: Menú principal del sistema
- user_view.py: Interfaz de gestión de usuarios
- payment_view.py: Interfaz de registro de pagos
- configuration_view.py: Interfaz de configuración

NOTA IMPORTANTE:
Las Views solo deben preocuparse por la presentación.
Toda la lógica debe estar en Controllers o Models.

=============================================================================
"""

# Importar las vistas principales para facilitar su uso
from .auth_view import AuthView
from .main_view import MainView

# Estas se importarán bajo demanda para ahorrar recursos
# from .user_view import UserManagementView
# from .payment_view import PaymentRegistrationView
# from .configuration_view import ConfigurationView

__all__ = [
    'AuthView',
    'MainView'
]
