#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
CONFIGURATION MODEL - MODELO DE CONFIGURACIÓN
=============================================================================

Este módulo maneja toda la configuración del sistema:
- Cuota mensual
- PIN de acceso
- Conceptos de cobro
- Información del comité

=============================================================================
"""

from typing import List, Dict, Optional
from .database import get_db_manager


class ConfigurationModel:
    """
    Modelo para la gestión de configuración del sistema.
    """
    
    def __init__(self):
        """Inicializa el modelo de configuración."""
        self.db = get_db_manager()
    
    # =============================================================================
    # CONFIGURACIÓN GENERAL
    # =============================================================================
    
    def obtener_configuracion(self, clave: str) -> Optional[str]:
        """
        Obtiene un valor de configuración por su clave.
        
        Args:
            clave: Nombre de la configuración (ej: 'cuota_mensual')
            
        Returns:
            Valor de la configuración o None si no existe
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'SELECT valor FROM configuracion WHERE clave = ?', 
                (clave,)
            )
            row = cursor.fetchone()
            return row[0] if row else None
            
        finally:
            conn.close()
    
    def actualizar_configuracion(self, clave: str, valor: str) -> bool:
        """
        Actualiza un valor de configuración.
        
        Args:
            clave: Nombre de la configuración
            valor: Nuevo valor
            
        Returns:
            True si se actualizó correctamente
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE configuracion 
                SET valor = ?, fecha_modificacion = CURRENT_TIMESTAMP
                WHERE clave = ?
            ''', (valor, clave))
            
            conn.commit()
            return cursor.rowcount > 0
            
        finally:
            conn.close()
    
    def verificar_pin(self, pin: str) -> bool:
        """
        Verifica si el PIN ingresado es correcto.
        
        Args:
            pin: PIN a verificar
            
        Returns:
            True si el PIN es correcto
        """
        pin_actual = self.obtener_configuracion('pin_acceso')
        return pin_actual == pin
    
    # =============================================================================
    # CONCEPTOS DE COBRO
    # =============================================================================
    
    def obtener_conceptos_cobro(self, solo_activos: bool = True) -> List[Dict]:
        """
        Obtiene todos los conceptos de cobro.
        
        Args:
            solo_activos: Si True, solo devuelve conceptos activos
            
        Returns:
            Lista de conceptos de cobro
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            if solo_activos:
                cursor.execute('''
                    SELECT * FROM conceptos_cobro 
                    WHERE activo = 1 
                    ORDER BY nombre
                ''')
            else:
                cursor.execute(
                    'SELECT * FROM conceptos_cobro ORDER BY nombre'
                )
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        finally:
            conn.close()
    
    def crear_concepto_cobro(self, nombre: str, precio: float) -> bool:
        """
        Crea un nuevo concepto de cobro.
        
        Args:
            nombre: Nombre del concepto
            precio: Precio del concepto
            
        Returns:
            True si se creó correctamente
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO conceptos_cobro (nombre, precio)
                VALUES (?, ?)
            ''', (nombre, precio))
            
            conn.commit()
            return True
            
        except Exception:
            # Ya existe un concepto con ese nombre
            return False
            
        finally:
            conn.close()
    
    def actualizar_concepto_cobro(self, concepto_id: int, nombre: str = None, 
                                 precio: float = None, activo: bool = None) -> bool:
        """
        Actualiza un concepto de cobro.
        
        Args:
            concepto_id: ID del concepto
            nombre: Nuevo nombre (opcional)
            precio: Nuevo precio (opcional)
            activo: Nuevo estado (opcional)
            
        Returns:
            True si se actualizó correctamente
        """
        campos_actualizar = {}
        
        if nombre is not None:
            campos_actualizar['nombre'] = nombre
        if precio is not None:
            campos_actualizar['precio'] = precio
        if activo is not None:
            campos_actualizar['activo'] = 1 if activo else 0
        
        if not campos_actualizar:
            return False
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            campos = list(campos_actualizar.keys())
            valores = list(campos_actualizar.values())
            valores.append(concepto_id)
            
            set_clause = ', '.join([f"{campo} = ?" for campo in campos])
            
            cursor.execute(f'''
                UPDATE conceptos_cobro 
                SET {set_clause}
                WHERE id = ?
            ''', valores)
            
            conn.commit()
            return cursor.rowcount > 0
            
        finally:
            conn.close()
