#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
PAQUETE MODELS - CAPA DE MODELOS (MVC)
=============================================================================

Este paquete contiene todos los modelos del sistema que representan
las entidades de negocio y la lógica de acceso a datos.

PATRÓN MVC:
- Los MODELS son responsables de:
  1. Definir la estructura de los datos
  2. Gestionar la conexión con la base de datos
  3. Realizar operaciones CRUD (Create, Read, Update, Delete)
  4. Aplicar reglas de negocio sobre los datos

ARCHIVOS DEL PAQUETE:
- database.py: Gestor principal de base de datos
- user_model.py: Modelo para la gestión de usuarios
- payment_model.py: Modelo para la gestión de pagos
- configuration_model.py: Modelo para la configuración del sistema

Autor: Tu Nombre
Fecha: 2025
=============================================================================
"""

# Importar los modelos principales para facilitar su uso
from .database import DatabaseManager, get_db_manager
from .user_model import UserModel
from .payment_model import PaymentModel
from .configuration_model import ConfigurationModel

# Definir qué se exporta cuando se hace: from models import *
__all__ = [
    'DatabaseManager',
    'get_db_manager',
    'UserModel',
    'PaymentModel',
    'ConfigurationModel'
]
