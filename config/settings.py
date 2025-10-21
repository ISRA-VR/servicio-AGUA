#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
CONFIGURACIÓN DEL SISTEMA
=============================================================================

Este archivo contiene todas las configuraciones y constantes del sistema.

USO:
    from config.settings import COLORS, DATABASE_NAME
    
    color_primario = COLORS['primary']

VENTAJAS:
- Centraliza todas las configuraciones
- Fácil de modificar
- No necesitas buscar valores en múltiples archivos

=============================================================================
"""

# =============================================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# =============================================================================

DATABASE_NAME = "agua_potable.db"
DATABASE_BACKUP_DIR = "backups"


# =============================================================================
# CONFIGURACIÓN DE LA INTERFAZ
# =============================================================================

# Paleta de colores del sistema
# Puedes cambiar estos valores para personalizar la apariencia
COLORS = {
    'primary': '#2980b9',      # Azul principal
    'secondary': '#3498db',    # Azul secundario
    'success': '#27ae60',      # Verde (éxito)
    'warning': '#f39c12',      # Naranja (advertencia)
    'danger': '#e74c3c',       # Rojo (error/peligro)
    'dark': '#2c3e50',         # Azul oscuro
    'light': '#ecf0f1',        # Gris claro
    'white': '#ffffff',        # Blanco
    'text': '#2c3e50',         # Color de texto principal
    'text_secondary': '#7f8c8d'  # Color de texto secundario
}

# Tamaños de ventana
WINDOW_SIZES = {
    'login': '400x300',
    'main': '900x650',
    'users': '1200x800',
    'payments': '1100x800',
    'config': '1000x700'
}

# Fuentes
FONTS = {
    'title': ('Arial', 16, 'bold'),
    'subtitle': ('Arial', 14, 'bold'),
    'normal': ('Arial', 11),
    'normal_bold': ('Arial', 11, 'bold'),
    'small': ('Arial', 9),
    'button': ('Arial', 12, 'bold')
}


# =============================================================================
# CONFIGURACIÓN DE RECIBOS
# =============================================================================

RECEIPT_DIR = "recibos"
LOGO_PATH = "logo.jpg"

# Información del comité para los recibos
COMMITTEE_INFO = {
    'name': 'COMITÉ DE AGUA POTABLE',
    'address': 'Dirección del Comité',
    'phone': 'Teléfono de Contacto',
    'email': 'correo@comiteagua.com'
}


# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD
# =============================================================================

# PIN por defecto (¡DEBE CAMBIARSE!)
DEFAULT_PIN = '1234'

# Longitud mínima y máxima del PIN
PIN_MIN_LENGTH = 4
PIN_MAX_LENGTH = 8


# =============================================================================
# CONFIGURACIÓN DE IMPORTACIÓN CSV
# =============================================================================

# Nombres de columnas aceptados en archivos CSV
CSV_COLUMN_MAPPING = {
    'numero': ['numero', 'num', 'number', 'id'],
    'nombre': ['nombre', 'name', 'usuario', 'user'],
    'direccion': ['direccion', 'address', 'domicilio', 'dir'],
    'telefono': ['telefono', 'phone', 'tel', 'celular'],
    'email': ['email', 'correo', 'mail', 'e-mail']
}


# =============================================================================
# CONFIGURACIÓN DE PAGOS
# =============================================================================

# Cuota mensual por defecto
DEFAULT_MONTHLY_FEE = 50.0

# Nombres de meses
MONTH_NAMES = [
    '', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]

# Conceptos de cobro predeterminados
DEFAULT_CONCEPTS = [
    ('Cooperación Anual', 100.0),
    ('Toma Nueva', 500.0),
    ('Multa por Inasistencia', 25.0),
    ('Multa por Desperdicio', 75.0),
    ('Reconexión', 150.0),
]


# =============================================================================
# MENSAJES DEL SISTEMA
# =============================================================================

MESSAGES = {
    'login_failed': 'PIN incorrecto. Intente nuevamente.',
    'login_success': 'Bienvenido al sistema',
    'user_created': 'Usuario creado exitosamente',
    'user_updated': 'Usuario actualizado exitosamente',
    'payment_registered': 'Pago registrado exitosamente',
    'error_generic': 'Ocurrió un error. Por favor intente nuevamente.',
}


# =============================================================================
# FUNCIONES DE UTILIDAD PARA CONFIGURACIÓN
# =============================================================================

def get_color(name: str) -> str:
    """
    Obtiene un color de la paleta por su nombre.
    
    Args:
        name: Nombre del color ('primary', 'success', etc.)
        
    Returns:
        Código hexadecimal del color
    """
    return COLORS.get(name, COLORS['primary'])


def get_font(name: str) -> tuple:
    """
    Obtiene una configuración de fuente por su nombre.
    
    Args:
        name: Nombre de la fuente ('title', 'normal', etc.)
        
    Returns:
        Tupla con configuración de fuente
    """
    return FONTS.get(name, FONTS['normal'])
