#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
DATABASE - GESTOR DE BASE DE DATOS
=============================================================================

Este módulo contiene la clase DatabaseManager que es responsable de:
1. Crear y mantener la conexión con la base de datos SQLite
2. Inicializar las tablas de la base de datos
3. Proporcionar métodos de acceso a datos para todas las entidades

PATRÓN SINGLETON:
Se utiliza el patrón Singleton para asegurar que solo exista una instancia
del gestor de base de datos en toda la aplicación.

TABLAS DE LA BASE DE DATOS:
- usuarios: Almacena información de los usuarios del servicio
- configuracion: Almacena parámetros de configuración del sistema
- conceptos_cobro: Almacena los conceptos de cobro adicionales
- pagos: Almacena el registro de pagos realizados
- detalle_pagos: Almacena el detalle de cada pago (meses y conceptos)

=============================================================================
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class DatabaseManager:
    """
    Clase principal para la gestión de la base de datos SQLite.
    
    Esta clase implementa el patrón Singleton y proporciona métodos
    para todas las operaciones de base de datos del sistema.
    """
    
    def __init__(self, db_path: str = "agua_potable.db"):
        """
        Inicializa el gestor de base de datos.
        
        Args:
            db_path (str): Ruta al archivo de la base de datos SQLite
                          Por defecto: "agua_potable.db" en el directorio actual
        """
        self.db_path = db_path
        # Inicializar la base de datos (crear tablas si no existen)
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Obtiene una nueva conexión a la base de datos.
        
        IMPORTANTE: Cada vez que llamamos a este método obtenemos una nueva
        conexión. Es responsabilidad del que llama cerrar la conexión.
        
        Returns:
            sqlite3.Connection: Objeto de conexión a la base de datos
        """
        # Crear la conexión
        conn = sqlite3.connect(self.db_path)
        
        # Configurar row_factory para que los resultados sean diccionarios
        # Esto facilita el acceso a los datos por nombre de columna
        conn.row_factory = sqlite3.Row
        
        return conn
    
    def init_database(self):
        """
        Inicializa las tablas de la base de datos si no existen.
        
        Este método se ejecuta automáticamente al crear una instancia de
        DatabaseManager y crea todas las tablas necesarias para el sistema.
        
        SEGURIDAD: Utiliza CREATE TABLE IF NOT EXISTS para no sobrescribir
        datos existentes.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # ====== TABLA DE USUARIOS ======
            # Almacena la información de todos los usuarios del servicio
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID único del usuario
                    numero INTEGER UNIQUE NOT NULL,         -- Número de usuario (debe ser único)
                    nombre TEXT NOT NULL,                   -- Nombre completo del usuario
                    direccion TEXT,                         -- Dirección física
                    telefono TEXT,                          -- Número de teléfono
                    email TEXT,                             -- Correo electrónico
                    estado TEXT DEFAULT 'Activo' CHECK (estado IN ('Activo', 'Cancelado')),  -- Estado del usuario
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Fecha de registro automática
                )
            ''')
            
            # ====== TABLA DE CONFIGURACIÓN ======
            # Almacena parámetros configurables del sistema
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS configuracion (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    clave TEXT UNIQUE NOT NULL,             -- Nombre de la configuración (ej: 'cuota_mensual')
                    valor TEXT NOT NULL,                    -- Valor de la configuración
                    descripcion TEXT,                       -- Descripción de qué hace esta configuración
                    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Última modificación
                )
            ''')
            
            # ====== TABLA DE CONCEPTOS DE COBRO ======
            # Almacena los conceptos adicionales que se pueden cobrar
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conceptos_cobro (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,            -- Nombre del concepto (ej: 'Multa por desperdicio')
                    precio REAL NOT NULL,                   -- Precio del concepto
                    activo BOOLEAN DEFAULT 1,               -- Si el concepto está activo o no
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # ====== TABLA DE PAGOS ======
            # Almacena el encabezado de cada pago realizado
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pagos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,            -- ID del usuario que realizó el pago
                    fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Fecha y hora del pago
                    total REAL NOT NULL,                    -- Monto total del pago
                    observaciones TEXT,                     -- Observaciones opcionales
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)  -- Relación con tabla usuarios
                )
            ''')
            
            # ====== TABLA DE DETALLE DE PAGOS ======
            # Almacena el detalle de cada pago (qué meses o conceptos se pagaron)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS detalle_pagos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pago_id INTEGER NOT NULL,               -- ID del pago principal
                    concepto TEXT NOT NULL,                 -- Descripción del concepto
                    mes INTEGER NULL,                       -- Mes pagado (NULL si no es mensualidad)
                    anio INTEGER NOT NULL,                  -- Año del pago
                    precio REAL NOT NULL,                   -- Precio unitario
                    cantidad INTEGER DEFAULT 1,             -- Cantidad (normalmente 1)
                    FOREIGN KEY (pago_id) REFERENCES pagos (id)  -- Relación con tabla pagos
                )
            ''')
            
            # ====== INSERTAR CONFIGURACIÓN INICIAL ======
            # Estos valores solo se insertan si no existen (INSERT OR IGNORE)
            
            # Cuota mensual por defecto: $50.00
            cursor.execute('''
                INSERT OR IGNORE INTO configuracion (clave, valor, descripcion)
                VALUES ('cuota_mensual', '50.0', 'Cuota mensual del servicio de agua')
            ''')
            
            # PIN de acceso por defecto: 1234 (DEBES CAMBIARLO!)
            cursor.execute('''
                INSERT OR IGNORE INTO configuracion (clave, valor, descripcion)
                VALUES ('pin_acceso', '1234', 'PIN de acceso al sistema')
            ''')
            
            # ====== INSERTAR CONCEPTOS DE COBRO PREDETERMINADOS ======
            # Lista de conceptos comunes en comités de agua
            conceptos_default = [
                ('Cooperación Anual', 100.0),
                ('Toma Nueva', 500.0),
                ('Multa por Inasistencia', 25.0),
                ('Multa por Desperdicio', 75.0),
                ('Reconexión', 150.0),
            ]
            
            # Insertar cada concepto (solo si no existe)
            for concepto, precio in conceptos_default:
                cursor.execute('''
                    INSERT OR IGNORE INTO conceptos_cobro (nombre, precio)
                    VALUES (?, ?)
                ''', (concepto, precio))
            
            # Confirmar todos los cambios
            conn.commit()
            
        except sqlite3.Error as e:
            # Si hay algún error, revertir todos los cambios
            print(f"Error al inicializar la base de datos: {e}")
            conn.rollback()
        finally:
            # Siempre cerrar la conexión
            conn.close()
    
    # =============================================================================
    # MÉTODOS DE UTILIDAD GENERAL
    # =============================================================================
    
    def ejecutar_consulta(self, query: str, params: tuple = ()) -> List[Dict]:
        """
        Ejecuta una consulta SELECT y devuelve los resultados.
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (tuple): Parámetros para la consulta (opcional)
            
        Returns:
            List[Dict]: Lista de diccionarios con los resultados
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
    
    def ejecutar_modificacion(self, query: str, params: tuple = ()) -> int:
        """
        Ejecuta una consulta de modificación (INSERT, UPDATE, DELETE).
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (tuple): Parámetros para la consulta
            
        Returns:
            int: Número de filas afectadas
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            conn.rollback()
            raise e
        finally:
            conn.close()


# =============================================================================
# PATRÓN SINGLETON - INSTANCIA GLOBAL DEL GESTOR
# =============================================================================

# Variable privada para almacenar la única instancia del gestor
_db_manager = None

def get_db_manager() -> DatabaseManager:
    """
    Obtiene la instancia global del gestor de base de datos.
    
    Esta función implementa el patrón Singleton: solo crea una instancia
    la primera vez que se llama, y luego siempre devuelve la misma instancia.
    
    USO:
        db = get_db_manager()
        usuarios = db.obtener_todos_usuarios()
    
    Returns:
        DatabaseManager: La única instancia del gestor de base de datos
    """
    global _db_manager
    
    # Si no existe la instancia, crearla
    if _db_manager is None:
        _db_manager = DatabaseManager()
    
    # Devolver la instancia (nueva o existente)
    return _db_manager
