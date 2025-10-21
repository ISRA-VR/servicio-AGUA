# 🚰 SISTEMA DE GESTIÓN DE AGUA POTABLE - PATRÓN MVC

## 📁 ESTRUCTURA DEL PROYECTO (Patrón MVC)

```
servicio-AGUA/
│
├── 📂 models/                  # CAPA DE MODELOS (Datos y lógica de negocio)
│   ├── __init__.py            # Inicializador del paquete
│   ├── database.py            # Gestor principal de base de datos
│   ├── user_model.py          # Modelo para usuarios
│   ├── payment_model.py       # Modelo para pagos
│   └── configuration_model.py # Modelo para configuración
│
├── 📂 views/                   # CAPA DE VISTAS (Interfaz de usuario)
│   ├── __init__.py            # Inicializador del paquete
│   ├── auth_view.py           # Vista de autenticación (Login)
│   ├── main_view.py           # Vista principal del sistema
│   ├── user_view.py           # Vista de gestión de usuarios
│   ├── payment_view.py        # Vista de registro de pagos
│   └── configuration_view.py  # Vista de configuración
│
├── 📂 controllers/             # CAPA DE CONTROLADORES (Lógica de control)
│   ├── __init__.py            # Inicializador del paquete
│   ├── user_controller.py     # Controlador de usuarios
│   ├── payment_controller.py  # Controlador de pagos
│   └── config_controller.py   # Controlador de configuración
│
├── 📂 utils/                   # UTILIDADES Y HERRAMIENTAS
│   ├── __init__.py            # Inicializador del paquete
│   ├── receipt_generator.py  # Generador de recibos PDF
│   └── csv_importer.py        # Importador de datos CSV
│
├── 📂 config/                  # ARCHIVOS DE CONFIGURACIÓN
│   └── settings.py            # Configuraciones del sistema
│
├── 📂 recibos/                 # CARPETA PARA RECIBOS GENERADOS
│
├── 🐍 main.py                  # PUNTO DE ENTRADA PRINCIPAL
├── 📊 agua_potable.db         # BASE DE DATOS SQLite
├── 📄 requirements.txt        # Dependencias de Python
└── 📖 README_MVC.md           # Este archivo

```

---

## 🎯 ¿QUÉ ES EL PATRÓN MVC?

MVC (Model-View-Controller) es un patrón de diseño que separa la aplicación en tres componentes principales:

### 1. 🗃️ MODEL (Modelo)
**Responsabilidad**: Gestionar los datos y la lógica de negocio

**¿Qué hace?**
- Se conecta a la base de datos
- Define cómo se estructuran los datos
- Realiza operaciones CRUD (Create, Read, Update, Delete)
- Aplica reglas de negocio

**En nuestro proyecto**:
- `database.py`: Conexión y gestión de la base de datos
- `user_model.py`: Todo lo relacionado con usuarios
- `payment_model.py`: Todo lo relacionado con pagos
- `configuration_model.py`: Configuración del sistema

**Ejemplo**:
```python
# En user_model.py
def crear_usuario(self, numero, nombre):
    # Lógica para guardar en la base de datos
    pass
```

---

### 2. 👁️ VIEW (Vista)
**Responsabilidad**: Mostrar la interfaz al usuario

**¿Qué hace?**
- Crea ventanas y formularios
- Muestra información al usuario
- Captura entrada del usuario (clicks, texto, etc.)
- NO contiene lógica de negocio (solo presentación)

**En nuestro proyecto**:
- `auth_view.py`: Pantalla de login
- `main_view.py`: Ventana principal
- `user_view.py`: Interfaz de gestión de usuarios
- `payment_view.py`: Interfaz de registro de pagos
- `configuration_view.py`: Interfaz de configuración

**Ejemplo**:
```python
# En user_view.py
def crear_formulario_usuario(self):
    # Crear campos de entrada
    # Crear botones
    # Mostrar información
    pass
```

---

### 3. 🎮 CONTROLLER (Controlador)
**Responsabilidad**: Conectar Model y View

**¿Qué hace?**
- Recibe acciones del usuario desde la View
- Procesa la lógica de control
- Llama a los Models para obtener/guardar datos
- Actualiza la View con los resultados

**En nuestro proyecto**:
- `user_controller.py`: Lógica de control de usuarios
- `payment_controller.py`: Lógica de control de pagos
- `config_controller.py`: Lógica de control de configuración

**Ejemplo**:
```python
# En user_controller.py
def guardar_usuario(self, datos_formulario):
    # 1. Validar datos
    # 2. Llamar al Model para guardar
    # 3. Actualizar la View con el resultado
    pass
```

---

## 🔄 FLUJO DE DATOS EN MVC

```
┌─────────────┐
│   USUARIO   │ (Hace click en "Guardar Usuario")
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    VIEW     │ (Captura los datos del formulario)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ CONTROLLER  │ (Valida y procesa los datos)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    MODEL    │ (Guarda en la base de datos)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ CONTROLLER  │ (Recibe confirmación)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    VIEW     │ (Muestra mensaje: "Usuario guardado")
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   USUARIO   │ (Ve el mensaje de éxito)
└─────────────┘
```

---

## 💡 VENTAJAS DE USAR MVC

### ✅ Organización
- Cada archivo tiene una responsabilidad clara
- Fácil encontrar dónde está cada cosa
- No más "código espaguetti"

### ✅ Mantenibilidad
- Si cambias la interfaz, solo modificas Views
- Si cambias la base de datos, solo modificas Models
- Si cambias la lógica, solo modificas Controllers

### ✅ Reutilización
- Puedes usar el mismo Model en diferentes Views
- Puedes cambiar la View sin tocar el Model

### ✅ Trabajo en equipo
- Una persona puede trabajar en Views
- Otra en Models
- Otra en Controllers
- Sin pisarse el código

### ✅ Pruebas
- Puedes probar cada capa por separado
- Más fácil detectar y arreglar errores

---

## 📚 EXPLICACIÓN DE CADA CARPETA

### 📂 models/ (DATOS)
**¿Cuándo modifico aquí?**
- Cuando necesito cambiar la estructura de la base de datos
- Cuando necesito agregar nuevas consultas SQL
- Cuando cambio reglas de negocio sobre datos

**Ejemplo de uso**:
```python
from models.user_model import UserModel

# Crear instancia del modelo
user_model = UserModel()

# Usar sus métodos
usuario = user_model.buscar_usuario_por_numero(100)
```

---

### 📂 views/ (INTERFAZ)
**¿Cuándo modifico aquí?**
- Cuando cambio el diseño de ventanas
- Cuando agrego o quito campos de formularios
- Cuando cambio colores, tamaños, posiciones

**Ejemplo de uso**:
```python
from views.user_view import UserManagementView

# Crear y mostrar la vista
vista = UserManagementView()
vista.mostrar()
```

---

### 📂 controllers/ (LÓGICA)
**¿Cuándo modifico aquí?**
- Cuando cambio el flujo de la aplicación
- Cuando agrego validaciones
- Cuando necesito coordinar múltiples Models

**Ejemplo de uso**:
```python
from controllers.user_controller import UserController

# Crear controlador
controller = UserController()

# Procesar acción
resultado = controller.crear_nuevo_usuario(datos)
```

---

### 📂 utils/ (HERRAMIENTAS)
**¿Cuándo modifico aquí?**
- Funciones auxiliares que no son Model, View o Controller
- Generadores de reportes
- Importadores/Exportadores
- Utilidades generales

---

## 🚀 CÓMO EJECUTAR EL SISTEMA

1. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar el sistema**:
   ```bash
   python main.py
   ```

3. **Login por defecto**:
   - PIN: `1234` (¡Cámbialo después!)

---

## 📖 CÓMO MODIFICAR EL CÓDIGO

### Ejemplo 1: Agregar un nuevo campo a Usuario

**1. Modificar el MODEL** (`models/user_model.py`):
```python
def crear_usuario(self, numero, nombre, nuevo_campo):
    # Agregar nuevo_campo a la consulta SQL
    pass
```

**2. Modificar la VIEW** (`views/user_view.py`):
```python
def crear_formulario(self):
    # Agregar un Entry para nuevo_campo
    self.nuevo_campo_entry = tk.Entry(...)
```

**3. Modificar el CONTROLLER** (`controllers/user_controller.py`):
```python
def guardar_usuario(self):
    # Capturar el nuevo_campo de la vista
    # Pasarlo al model
    pass
```

---

### Ejemplo 2: Cambiar el color de un botón

**Solo modificas la VIEW**:
```python
# En views/user_view.py
boton = tk.Button(
    text="Guardar",
    bg='#27ae60',  # Cambiar este color
    fg='white'
)
```

---

### Ejemplo 3: Agregar validación

**Modificas el CONTROLLER**:
```python
# En controllers/user_controller.py
def validar_telefono(self, telefono):
    if len(telefono) < 10:
        return False, "Teléfono debe tener 10 dígitos"
    return True, "OK"
```

---

## 🎓 CONCEPTOS IMPORTANTES

### 🔒 Principio de Responsabilidad Única
Cada clase debe tener una sola responsabilidad:
- UserModel: Solo se encarga de usuarios
- PaymentView: Solo muestra la interfaz de pagos
- UserController: Solo coordina lógica de usuarios

### 🔗 Bajo Acoplamiento
Las capas están separadas:
- View no conoce los detalles de la base de datos
- Model no conoce los detalles de la interfaz
- Controller los conecta sin que se conozcan directamente

### 📦 Alta Cohesión
Todo lo relacionado está junto:
- Todo sobre usuarios en user_model.py
- Todo sobre la vista de pagos en payment_view.py

---

## 🐛 SOLUCIÓN DE PROBLEMAS COMUNES

### ❌ Error: "No se puede importar models"
**Solución**: Asegúrate de que `__init__.py` existe en la carpeta models

### ❌ Error: "No se encuentra la base de datos"
**Solución**: El archivo `agua_potable.db` se crea automáticamente en la primera ejecución

### ❌ La ventana no se muestra
**Solución**: Verifica que estés llamando a `root.mainloop()` al final

---

## 📞 CONTACTO Y SOPORTE

Para preguntas sobre el código:
1. Lee los comentarios en cada archivo
2. Revisa este README
3. Consulta la documentación de Python/Tkinter

---

## 📝 NOTAS FINALES

- **Siempre comenta tu código**: Explica QUÉ hace y POR QUÉ
- **Usa nombres descriptivos**: `calcular_total_pago` es mejor que `calc`
- **Prueba cada cambio**: Ejecuta el programa después de cada modificación
- **Haz respaldos**: Guarda copias de la base de datos regularmente

---

**¡Feliz codificación! 🎉**

> Recuerda: El código limpio es fácil de leer, entender y modificar.
> Con MVC, mantienes tu código organizado y profesional.
