#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
PAQUETE UTILS - UTILIDADES Y HERRAMIENTAS
=============================================================================

Este paquete contiene funciones y clases auxiliares que no son
parte directa del patrón MVC pero son necesarias para el sistema.

CONTENIDO:
- receipt_generator.py: Generador de recibos en PDF
- csv_importer.py: Importador de datos desde archivos CSV
- helpers.py: Funciones auxiliares generales

NOTA:
Las utilidades pueden ser usadas por cualquier capa (Model, View o Controller)

=============================================================================
"""

from .receipt_generator import ReceiptGenerator
from .csv_importer import CSVImporter, ImporterGUI

__all__ = [
    'ReceiptGenerator',
    'CSVImporter',
    'ImporterGUI'
]
