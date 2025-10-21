#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
SCRIPT DE MIGRACIÓN AUTOMÁTICA A ESTRUCTURA MVC
=============================================================================

Este script te ayuda a reorganizar tu proyecto a la estructura MVC
de forma automática y segura.

FUNCIONALIDADES:
1. Crea copia de seguridad de archivos importantes
2. Copia archivos a su nueva ubicación
3. Actualiza imports automáticamente
4. Genera reporte de cambios

USO:
    python migrate_to_mvc.py

SEGURIDAD:
- No elimina archivos originales
- Crea backups antes de modificar
- Puedes revertir cambios fácilmente

=============================================================================
"""

import os
import shutil
from datetime import datetime
from pathlib import Path


class MVCMigrator:
    """
    Clase para migrar el proyecto a estructura MVC.
    """
    
    def __init__(self):
        """
        Inicializa el migrador.
        """
        self.project_root = Path(__file__).parent
        self.backup_dir = self.project_root / "backup_pre_mvc"
        self.report = []
        
    def log(self, message: str, level: str = "INFO"):
        """
        Registra un mensaje en el reporte.
        
        Args:
            message: Mensaje a registrar
            level: Nivel (INFO, SUCCESS, WARNING, ERROR)
        """
        emoji = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌"
        }.get(level, "•")
        
        msg = f"{emoji} {message}"
        print(msg)
        self.report.append(msg)
    
    def create_backup(self):
        """
        Crea copia de seguridad de archivos importantes.
        """
        self.log("Creando copia de seguridad...", "INFO")
        
        # Crear directorio de backup si no existe
        if not self.backup_dir.exists():
            self.backup_dir.mkdir()
        
        # Archivos a respaldar
        files_to_backup = [
            "agua_potable.db",
            "database.py",
            "auth.py",
            "main.py",
            "user_management.py",
            "payment_registration.py",
            "configuration.py",
            "receipt_generator.py",
            "csv_importer.py"
        ]
        
        backup_count = 0
        for filename in files_to_backup:
            source = self.project_root / filename
            if source.exists():
                dest = self.backup_dir / filename
                shutil.copy2(source, dest)
                backup_count += 1
                self.log(f"Respaldado: {filename}", "SUCCESS")
        
        self.log(f"Total de archivos respaldados: {backup_count}", "SUCCESS")
    
    def copy_utils(self):
        """
        Copia archivos de utilidades a la carpeta utils/
        """
        self.log("Copiando utilidades...", "INFO")
        
        utils_files = [
            ("receipt_generator.py", "utils/receipt_generator.py"),
            ("csv_importer.py", "utils/csv_importer.py")
        ]
        
        for source_name, dest_path in utils_files:
            source = self.project_root / source_name
            dest = self.project_root / dest_path
            
            if source.exists():
                shutil.copy2(source, dest)
                self.log(f"Copiado: {source_name} → {dest_path}", "SUCCESS")
                
                # Actualizar imports en el archivo copiado
                self.update_imports_in_file(dest)
            else:
                self.log(f"No encontrado: {source_name}", "WARNING")
    
    def update_imports_in_file(self, filepath: Path):
        """
        Actualiza los imports en un archivo para usar la nueva estructura.
        
        Args:
            filepath: Ruta del archivo a actualizar
        """
        try:
            # Leer el contenido del archivo
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Reemplazos de imports
            replacements = {
                'from database import': 'from models.database import',
                'import database': 'from models import database',
            }
            
            # Aplicar reemplazos
            modified = False
            for old, new in replacements.items():
                if old in content:
                    content = content.replace(old, new)
                    modified = True
            
            # Si hubo cambios, guardar el archivo
            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.log(f"Imports actualizados en: {filepath.name}", "SUCCESS")
        
        except Exception as e:
            self.log(f"Error al actualizar imports en {filepath.name}: {e}", "ERROR")
    
    def verify_structure(self):
        """
        Verifica que la estructura de carpetas MVC esté completa.
        """
        self.log("Verificando estructura MVC...", "INFO")
        
        required_dirs = [
            "models",
            "views",
            "controllers",
            "utils",
            "config",
            "recibos"
        ]
        
        required_files = [
            "models/__init__.py",
            "models/database.py",
            "models/user_model.py",
            "models/payment_model.py",
            "models/configuration_model.py",
            "views/__init__.py",
            "controllers/__init__.py",
            "utils/__init__.py",
            "config/settings.py",
            "main_mvc.py"
        ]
        
        # Verificar directorios
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                self.log(f"Directorio OK: {dir_name}/", "SUCCESS")
            else:
                self.log(f"Falta directorio: {dir_name}/", "WARNING")
        
        # Verificar archivos
        for file_path in required_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                self.log(f"Archivo OK: {file_path}", "SUCCESS")
            else:
                self.log(f"Falta archivo: {file_path}", "WARNING")
    
    def generate_report(self):
        """
        Genera un reporte de la migración.
        """
        report_file = self.project_root / "migracion_reporte.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("REPORTE DE MIGRACIÓN A ESTRUCTURA MVC\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Proyecto: {self.project_root}\n\n")
            f.write("=" * 70 + "\n")
            f.write("ACCIONES REALIZADAS:\n")
            f.write("=" * 70 + "\n\n")
            
            for line in self.report:
                f.write(line + "\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write("PRÓXIMOS PASOS:\n")
            f.write("=" * 70 + "\n\n")
            f.write("1. Revisa este reporte para verificar que todo está correcto\n")
            f.write("2. Lee README_MVC.md para entender la nueva estructura\n")
            f.write("3. Lee GUIA_MIGRACION.md para instrucciones detalladas\n")
            f.write("4. Prueba el sistema con: python main_mvc.py\n")
            f.write("5. Si algo sale mal, restaura desde: backup_pre_mvc/\n\n")
        
        self.log(f"Reporte guardado en: {report_file.name}", "SUCCESS")
    
    def run(self):
        """
        Ejecuta el proceso completo de migración.
        """
        print("\n" + "=" * 70)
        print("🚀 MIGRADOR AUTOMÁTICO A ESTRUCTURA MVC")
        print("=" * 70 + "\n")
        
        print("Este script te ayudará a reorganizar tu proyecto.")
        print("No se eliminarán archivos originales.\n")
        
        respuesta = input("¿Deseas continuar? (s/n): ").lower()
        
        if respuesta != 's':
            print("\n❌ Migración cancelada por el usuario.")
            return
        
        print("\n" + "=" * 70 + "\n")
        
        # Ejecutar pasos
        try:
            self.create_backup()
            print()
            
            self.copy_utils()
            print()
            
            self.verify_structure()
            print()
            
            self.generate_report()
            print()
            
            print("=" * 70)
            print("✅ MIGRACIÓN COMPLETADA")
            print("=" * 70)
            print(f"\n📄 Revisa el archivo 'migracion_reporte.txt' para más detalles.")
            print(f"💾 Backup creado en: backup_pre_mvc/\n")
            print("PRÓXIMOS PASOS:")
            print("  1. Lee README_MVC.md")
            print("  2. Prueba: python main_mvc.py")
            print("  3. Si hay problemas, revisa GUIA_MIGRACION.md\n")
            
        except Exception as e:
            print(f"\n❌ Error durante la migración: {e}")
            print("💡 Revisa el reporte para más detalles.")


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    migrator = MVCMigrator()
    migrator.run()
