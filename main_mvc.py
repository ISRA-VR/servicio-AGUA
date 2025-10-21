#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
SISTEMA DE GESTIÓN DE AGUA POTABLE
=============================================================================

Archivo: main.py
Descripción: Punto de entrada principal del sistema

Este es el archivo que debes ejecutar para iniciar la aplicación.
Coordina el flujo principal del programa utilizando el patrón MVC.

FLUJO DEL PROGRAMA:
1. Se ejecuta la función main()
2. Se muestra la pantalla de autenticación (auth_view)
3. Si la autenticación es exitosa, se muestra el menú principal (main_view)
4. El usuario puede navegar entre los diferentes módulos

PATRÓN MVC APLICADO:
- Este archivo actúa como orquestador principal
- Llama a las Views para mostrar la interfaz
- Las Views usan Controllers para procesar acciones
- Los Controllers usan Models para acceder a datos

CÓMO EJECUTAR:
    python main.py

Autor: Tu Nombre
Fecha: 2025
Versión: 2.0 (Reorganizado con patrón MVC)
=============================================================================
"""

import sys
import tkinter as tk
from tkinter import messagebox

# Importar la vista de autenticación
from views.auth_view import AuthView

# Importar la vista principal
from views.main_view import MainView


def main():
    """
    Función principal del sistema.
    
    Esta función es el punto de entrada de toda la aplicación.
    Coordina el flujo desde el login hasta el menú principal.
    
    FLUJO:
    1. Intentar autenticar al usuario
    2. Si la autenticación es exitosa, mostrar el menú principal
    3. Si falla, cerrar la aplicación
    
    Returns:
        None
    """
    
    try:
        # ===================================================================
        # PASO 1: AUTENTICACIÓN
        # ===================================================================
        print("🔐 Iniciando sistema de autenticación...")
        
        # Crear instancia de la vista de autenticación
        # Esta vista mostrará una ventana para ingresar el PIN
        auth_view = AuthView()
        
        # Mostrar la ventana de login y esperar a que el usuario ingrese el PIN
        # El método show() devuelve True si el login fue exitoso, False si no
        autenticado = auth_view.show()
        
        # Verificar si la autenticación fue exitosa
        if not autenticado:
            print("❌ Autenticación fallida. Cerrando aplicación.")
            return  # Salir de la función (terminar el programa)
        
        print("✅ Autenticación exitosa!")
        
        # ===================================================================
        # PASO 2: MOSTRAR MENÚ PRINCIPAL
        # ===================================================================
        print("🏠 Cargando menú principal...")
        
        # Crear instancia de la vista principal
        # Esta vista mostrará el menú con todos los módulos del sistema
        main_view = MainView()
        
        # Ejecutar el bucle principal de la interfaz gráfica
        # Este método mantiene la ventana abierta y respondiendo a eventos
        main_view.run()
        
        print("👋 Sistema cerrado correctamente.")
        
    except Exception as e:
        # Si ocurre algún error inesperado, mostrarlo
        print(f"💥 Error fatal en el sistema: {str(e)}")
        
        # Mostrar un mensaje de error al usuario
        messagebox.showerror(
            "Error Fatal",
            f"Ocurrió un error inesperado:\n\n{str(e)}\n\nLa aplicación se cerrará."
        )
        
        # Registrar el error en un archivo de log (opcional)
        # with open('error.log', 'a') as f:
        #     f.write(f"{datetime.now()}: {str(e)}\n")


def verificar_dependencias():
    """
    Verifica que todas las dependencias necesarias estén instaladas.
    
    Esta función opcional se puede llamar antes de main() para
    asegurar que el sistema puede ejecutarse correctamente.
    
    Returns:
        bool: True si todas las dependencias están presentes
    """
    dependencias_requeridas = [
        ('tkinter', 'Tkinter (interfaz gráfica)'),
        ('PIL', 'Pillow (manejo de imágenes)'),
        ('reportlab', 'ReportLab (generación de PDFs)'),
    ]
    
    dependencias_faltantes = []
    
    # Intentar importar cada dependencia
    for modulo, nombre in dependencias_requeridas:
        try:
            __import__(modulo)
            print(f"✅ {nombre}: Instalado")
        except ImportError:
            print(f"❌ {nombre}: NO INSTALADO")
            dependencias_faltantes.append(nombre)
    
    # Si faltan dependencias, mostrar instrucciones
    if dependencias_faltantes:
        print("\n⚠️  DEPENDENCIAS FALTANTES:")
        print("Ejecuta: pip install -r requirements.txt")
        print("\nO instala manualmente:")
        for dep in dependencias_faltantes:
            print(f"  pip install {dep.split('(')[0].strip()}")
        return False
    
    print("\n✅ Todas las dependencias están instaladas correctamente\n")
    return True


def mostrar_banner():
    """
    Muestra un banner de bienvenida en la consola.
    
    Esta función es opcional y puramente estética.
    Muestra información sobre el sistema al iniciar.
    """
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║         💧 SISTEMA DE GESTIÓN DE AGUA POTABLE 💧             ║
    ║                                                               ║
    ║                   Versión 2.0 Professional                    ║
    ║                   Arquitectura: MVC Pattern                   ║
    ║                                                               ║
    ║         Desarrollado para Comités de Agua Potable            ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    
    📚 MÓDULOS DISPONIBLES:
       • Gestión de Usuarios
       • Registro de Pagos
       • Generación de Recibos
       • Configuración del Sistema
       • Importación de Datos CSV
    
    ═══════════════════════════════════════════════════════════════════
    """
    print(banner)


# =============================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# =============================================================================

if __name__ == "__main__":
    """
    Este bloque solo se ejecuta cuando se ejecuta este archivo directamente.
    No se ejecuta si este archivo es importado por otro módulo.
    
    FLUJO:
    1. Mostrar banner de bienvenida
    2. Verificar dependencias (opcional)
    3. Ejecutar la función principal
    """
    
    # Mostrar banner de bienvenida
    mostrar_banner()
    
    # Verificar que todas las dependencias estén instaladas
    # Comentar esta línea si quieres que el sistema inicie más rápido
    # if not verificar_dependencias():
    #     input("\nPresiona Enter para salir...")
    #     sys.exit(1)
    
    # Ejecutar el sistema
    main()
