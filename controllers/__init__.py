#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
PAQUETE CONTROLLERS - CAPA DE CONTROLADORES (MVC)
=============================================================================

Este paquete contiene los controladores que conectan Views y Models.

RESPONSABILIDAD DE LOS CONTROLLERS:
- Recibir acciones del usuario desde las Views
- Validar datos de entrada
- Llamar a los Models para obtener/modificar datos
- Actualizar las Views con los resultados
- Coordinar múltiples Models si es necesario

ARCHIVOS DEL PAQUETE:
- user_controller.py: Lógica de control de usuarios
- payment_controller.py: Lógica de control de pagos
- config_controller.py: Lógica de control de configuración

PATRÓN:
View → llama a → Controller → llama a → Model
Model → devuelve datos → Controller → actualiza → View

=============================================================================
"""

# Los controladores se importan bajo demanda
# from .user_controller import UserController
# from .payment_controller import PaymentController
# from .config_controller import ConfigController

__all__ = [
    'UserController',
    'PaymentController',
    'ConfigController'
]
