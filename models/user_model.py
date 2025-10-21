#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
USER MODEL - MODELO DE USUARIOS
=============================================================================

Este módulo contiene la clase UserModel que maneja toda la lógica de
negocio relacionada con los usuarios del sistema.

RESPONSABILIDADES:
1. Crear nuevos usuarios
2. Buscar usuarios por diferentes criterios
3. Actualizar información de usuarios
4. Cambiar estados de usuarios (Activo/Cancelado)
5. Obtener listas de usuarios

PATRÓN DE DISEÑO:
Este modelo sigue el patrón Repository, encapsulando toda la lógica
de acceso a datos relacionada con usuarios.

=============================================================================
"""

from typing import List, Dict, Optional
from .database import get_db_manager


class UserModel:
    """
    Modelo para la gestión de usuarios del sistema de agua potable.
    
    Esta clase proporciona métodos para todas las operaciones relacionadas
    con usuarios sin exponer los detalles de implementación de la base de datos.
    """
    
    def __init__(self):
        """
        Inicializa el modelo de usuarios.
        
        Obtiene una referencia al gestor de base de datos para realizar
        todas las operaciones necesarias.
        """
        self.db = get_db_manager()
    
    # =============================================================================
    # MÉTODOS DE CREACIÓN
    # =============================================================================
    
    def crear_usuario(self, numero: int, nombre: str, direccion: str = "", 
                     telefono: str = "", email: str = "") -> bool:
        """
        Crea un nuevo usuario en el sistema.
        
        VALIDACIÓN:
        - El número de usuario debe ser único
        - El nombre es obligatorio
        
        Args:
            numero (int): Número único del usuario
            nombre (str): Nombre completo del usuario
            direccion (str, opcional): Dirección del usuario
            telefono (str, opcional): Teléfono del usuario
            email (str, opcional): Email del usuario
            
        Returns:
            bool: True si se creó exitosamente, False si ya existe el número
            
        Ejemplo:
            >>> user_model = UserModel()
            >>> exito = user_model.crear_usuario(100, "Juan Pérez", "Calle 123")
            >>> if exito:
            >>>     print("Usuario creado correctamente")
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Intentar insertar el nuevo usuario
            cursor.execute('''
                INSERT INTO usuarios (numero, nombre, direccion, telefono, email)
                VALUES (?, ?, ?, ?, ?)
            ''', (numero, nombre, direccion, telefono, email))
            
            # Confirmar la transacción
            conn.commit()
            return True
            
        except Exception as e:
            # Si el número ya existe, se lanzará una excepción de integridad
            print(f"Error al crear usuario: {e}")
            return False
            
        finally:
            # Siempre cerrar la conexión
            conn.close()
    
    def get_next_user_number(self) -> int:
        """
        Obtiene el siguiente número de usuario disponible.
        
        Este método busca el número más alto en la base de datos y
        devuelve el siguiente número secuencial.
        
        Returns:
            int: El siguiente número de usuario disponible
            
        Ejemplo:
            >>> user_model = UserModel()
            >>> next_num = user_model.get_next_user_number()
            >>> print(f"El próximo usuario será el número {next_num}")
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Buscar el número más alto actual
            cursor.execute('SELECT MAX(numero) FROM usuarios')
            result = cursor.fetchone()
            
            # Si no hay usuarios, empezar en 1
            # Si hay usuarios, devolver el máximo + 1
            max_number = result[0] if result and result[0] is not None else 0
            return max_number + 1
            
        finally:
            conn.close()
    
    # =============================================================================
    # MÉTODOS DE BÚSQUEDA
    # =============================================================================
    
    def buscar_usuario_por_numero(self, numero: int) -> Optional[Dict]:
        """
        Busca un usuario específico por su número.
        
        Args:
            numero (int): Número del usuario a buscar
            
        Returns:
            Optional[Dict]: Diccionario con los datos del usuario si se encuentra,
                           None si no existe
                           
        Ejemplo:
            >>> user_model = UserModel()
            >>> usuario = user_model.buscar_usuario_por_numero(100)
            >>> if usuario:
            >>>     print(f"Usuario encontrado: {usuario['nombre']}")
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM usuarios WHERE numero = ?', (numero,))
            row = cursor.fetchone()
            
            # Si se encontró el usuario, convertir a diccionario
            return dict(row) if row else None
            
        finally:
            conn.close()
    
    def buscar_usuarios_por_nombre(self, nombre: str) -> List[Dict]:
        """
        Busca usuarios por nombre (búsqueda parcial).
        
        Esta búsqueda es flexible: encuentra usuarios cuyo nombre
        contenga el texto proporcionado (no importa mayúsculas/minúsculas).
        
        Args:
            nombre (str): Texto a buscar en los nombres
            
        Returns:
            List[Dict]: Lista de usuarios que coinciden con la búsqueda
            
        Ejemplo:
            >>> user_model = UserModel()
            >>> usuarios = user_model.buscar_usuarios_por_nombre("Juan")
            >>> for usuario in usuarios:
            >>>     print(usuario['nombre'])
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # El símbolo % permite búsqueda parcial
            # Ejemplo: "Juan" encontrará "Juan Pérez", "María Juan", etc.
            cursor.execute('''
                SELECT * FROM usuarios 
                WHERE nombre LIKE ? 
                ORDER BY nombre
            ''', (f'%{nombre}%',))
            
            rows = cursor.fetchall()
            
            # Convertir todas las filas a diccionarios
            return [dict(row) for row in rows]
            
        finally:
            conn.close()
    
    def obtener_todos_usuarios(self, solo_activos: bool = False) -> List[Dict]:
        """
        Obtiene todos los usuarios del sistema.
        
        Args:
            solo_activos (bool): Si es True, solo devuelve usuarios activos
                                Si es False, devuelve todos los usuarios
            
        Returns:
            List[Dict]: Lista de todos los usuarios
            
        Ejemplo:
            >>> user_model = UserModel()
            >>> # Obtener solo usuarios activos
            >>> activos = user_model.obtener_todos_usuarios(solo_activos=True)
            >>> # Obtener todos los usuarios
            >>> todos = user_model.obtener_todos_usuarios()
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            if solo_activos:
                # Solo usuarios con estado 'Activo'
                cursor.execute('''
                    SELECT * FROM usuarios 
                    WHERE estado = 'Activo' 
                    ORDER BY numero
                ''')
            else:
                # Todos los usuarios
                cursor.execute('SELECT * FROM usuarios ORDER BY numero')
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        finally:
            conn.close()
    
    # =============================================================================
    # MÉTODOS DE ACTUALIZACIÓN
    # =============================================================================
    
    def actualizar_usuario(self, usuario_id: int, **kwargs) -> bool:
        """
        Actualiza los datos de un usuario existente.
        
        Este método es flexible: solo actualiza los campos que se proporcionen.
        
        Args:
            usuario_id (int): ID del usuario a actualizar
            **kwargs: Campos a actualizar (numero, nombre, direccion, telefono, email, estado)
            
        Returns:
            bool: True si se actualizó correctamente, False si no se encontró el usuario
            
        Ejemplo:
            >>> user_model = UserModel()
            >>> # Actualizar solo el teléfono
            >>> user_model.actualizar_usuario(1, telefono="555-1234")
            >>> # Actualizar múltiples campos
            >>> user_model.actualizar_usuario(1, 
            >>>     telefono="555-1234",
            >>>     email="nuevo@email.com")
        """
        # Si no se proporcionaron campos para actualizar, no hacer nada
        if not kwargs:
            return False
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Construir la consulta dinámicamente
            # Esto nos permite actualizar solo los campos especificados
            campos = list(kwargs.keys())
            valores = list(kwargs.values())
            valores.append(usuario_id)  # Agregar el ID al final
            
            # Crear la parte "SET campo1 = ?, campo2 = ?, ..."
            set_clause = ', '.join([f"{campo} = ?" for campo in campos])
            
            # Ejecutar la actualización
            cursor.execute(f'''
                UPDATE usuarios 
                SET {set_clause}
                WHERE id = ?
            ''', valores)
            
            conn.commit()
            
            # Verificar si se actualizó algún registro
            return cursor.rowcount > 0
            
        finally:
            conn.close()
    
    def cambiar_estado_usuario(self, usuario_id: int, estado: str) -> bool:
        """
        Cambia el estado de un usuario (Activo/Cancelado).
        
        Args:
            usuario_id (int): ID del usuario
            estado (str): Nuevo estado ('Activo' o 'Cancelado')
            
        Returns:
            bool: True si se cambió correctamente, False si el estado es inválido
            
        Ejemplo:
            >>> user_model = UserModel()
            >>> # Cancelar un usuario
            >>> user_model.cambiar_estado_usuario(1, 'Cancelado')
            >>> # Reactivar un usuario
            >>> user_model.cambiar_estado_usuario(1, 'Activo')
        """
        # Validar que el estado sea válido
        if estado not in ['Activo', 'Cancelado']:
            print(f"Error: Estado '{estado}' no válido. Usar 'Activo' o 'Cancelado'.")
            return False
        
        # Usar el método general de actualización
        return self.actualizar_usuario(usuario_id, estado=estado)
