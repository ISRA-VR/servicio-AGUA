#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
PAYMENT MODEL - MODELO DE PAGOS
=============================================================================

Este módulo contiene la lógica de negocio relacionada con los pagos:
- Registro de pagos mensuales
- Registro de conceptos adicionales
- Consulta de historial de pagos
- Obtención de meses pagados por usuario

=============================================================================
"""

from typing import List, Dict, Tuple, Optional
from .database import get_db_manager


class PaymentModel:
    """
    Modelo para la gestión de pagos del sistema.
    """
    
    def __init__(self):
        """Inicializa el modelo de pagos."""
        self.db = get_db_manager()
    
    def obtener_pagos_usuario_anio(self, usuario_id: int, anio: int) -> List[int]:
        """
        Obtiene los meses pagados por un usuario en un año específico.
        
        Args:
            usuario_id: ID del usuario
            anio: Año a consultar
            
        Returns:
            Lista de meses pagados (números del 1 al 12)
            
        Ejemplo:
            >>> payment_model = PaymentModel()
            >>> meses = payment_model.obtener_pagos_usuario_anio(1, 2024)
            >>> print(f"Meses pagados: {meses}")  # Ej: [1, 2, 3, 6]
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Buscar todos los meses pagados por el usuario en el año
            cursor.execute('''
                SELECT DISTINCT mes 
                FROM detalle_pagos dp
                JOIN pagos p ON dp.pago_id = p.id
                WHERE p.usuario_id = ? AND dp.anio = ? AND dp.mes IS NOT NULL
                ORDER BY mes
            ''', (usuario_id, anio))
            
            rows = cursor.fetchall()
            # Devolver solo los números de mes
            return [row[0] for row in rows]
            
        finally:
            conn.close()
    
    def registrar_pago(self, usuario_id: int, meses_pagados: List[int], anio: int,
                      conceptos_adicionales: List[Tuple[str, float]] = None,
                      observaciones: str = "") -> int:
        """
        Registra un nuevo pago completo.
        
        Este método crea:
        1. Un registro de pago principal
        2. Registros de detalle para cada mes pagado
        3. Registros de detalle para conceptos adicionales
        
        Args:
            usuario_id: ID del usuario que realiza el pago
            meses_pagados: Lista de números de mes (1-12)
            anio: Año de los pagos
            conceptos_adicionales: Lista de tuplas (nombre_concepto, precio)
            observaciones: Texto opcional con observaciones
            
        Returns:
            ID del pago registrado, 0 si hubo error
            
        Ejemplo:
            >>> payment_model = PaymentModel()
            >>> pago_id = payment_model.registrar_pago(
            >>>     usuario_id=1,
            >>>     meses_pagados=[1, 2, 3],  # Enero, Febrero, Marzo
            >>>     anio=2024,
            >>>     conceptos_adicionales=[("Multa", 50.0)],
            >>>     observaciones="Pago con retraso"
            >>> )
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # 1. Obtener la cuota mensual actual
            cursor.execute(
                "SELECT valor FROM configuracion WHERE clave = 'cuota_mensual'"
            )
            result = cursor.fetchone()
            cuota_mensual = float(result[0]) if result else 50.0
            
            # 2. Calcular el total del pago
            total = len(meses_pagados) * cuota_mensual
            if conceptos_adicionales:
                total += sum(precio for _, precio in conceptos_adicionales)
            
            # 3. Insertar el registro principal del pago
            cursor.execute('''
                INSERT INTO pagos (usuario_id, total, observaciones)
                VALUES (?, ?, ?)
            ''', (usuario_id, total, observaciones))
            
            # Obtener el ID del pago recién creado
            pago_id = cursor.lastrowid
            
            # 4. Insertar los detalles de mensualidades
            for mes in meses_pagados:
                cursor.execute('''
                    INSERT INTO detalle_pagos (pago_id, concepto, mes, anio, precio)
                    VALUES (?, ?, ?, ?, ?)
                ''', (pago_id, 'Mensualidad', mes, anio, cuota_mensual))
            
            # 5. Insertar los conceptos adicionales
            if conceptos_adicionales:
                for concepto, precio in conceptos_adicionales:
                    cursor.execute('''
                        INSERT INTO detalle_pagos (pago_id, concepto, mes, anio, precio)
                        VALUES (?, ?, NULL, ?, ?)
                    ''', (pago_id, concepto, anio, precio))
            
            # 6. Confirmar toda la transacción
            conn.commit()
            return pago_id
            
        except Exception as e:
            print(f"Error al registrar pago: {e}")
            conn.rollback()
            return 0
            
        finally:
            conn.close()
    
    def obtener_historial_pagos_usuario(self, usuario_id: int) -> List[Dict]:
        """
        Obtiene el historial completo de pagos de un usuario.
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            Lista de pagos con sus detalles
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Obtener todos los pagos del usuario
            cursor.execute('''
                SELECT p.*, u.nombre, u.numero
                FROM pagos p
                JOIN usuarios u ON p.usuario_id = u.id
                WHERE p.usuario_id = ?
                ORDER BY p.fecha_pago DESC
            ''', (usuario_id,))
            
            rows = cursor.fetchall()
            pagos = [dict(row) for row in rows]
            
            # Para cada pago, obtener sus detalles
            for pago in pagos:
                cursor.execute('''
                    SELECT * FROM detalle_pagos 
                    WHERE pago_id = ?
                    ORDER BY mes
                ''', (pago['id'],))
                
                detalles = cursor.fetchall()
                pago['detalles'] = [dict(detalle) for detalle in detalles]
            
            return pagos
            
        finally:
            conn.close()
    
    def obtener_detalle_pago(self, pago_id: int) -> Dict:
        """
        Obtiene el detalle completo de un pago específico.
        
        Este método es útil para generar recibos.
        
        Args:
            pago_id: ID del pago
            
        Returns:
            Diccionario con toda la información del pago
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Obtener información del pago y usuario
            cursor.execute('''
                SELECT p.*, u.nombre, u.numero, u.direccion
                FROM pagos p
                JOIN usuarios u ON p.usuario_id = u.id
                WHERE p.id = ?
            ''', (pago_id,))
            
            pago_row = cursor.fetchone()
            if not pago_row:
                return {}
            
            pago = dict(pago_row)
            
            # Obtener detalles del pago
            cursor.execute('''
                SELECT * FROM detalle_pagos 
                WHERE pago_id = ?
                ORDER BY mes, concepto
            ''', (pago_id,))
            
            detalles = cursor.fetchall()
            pago['detalles'] = [dict(detalle) for detalle in detalles]
            
            return pago
            
        finally:
            conn.close()
