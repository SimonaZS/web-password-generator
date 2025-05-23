# Web Password Generator - Estilo Hacker

Generador web de contraseñas seguras con interfaz estilo hacker, cifrado simple y gestión de favoritos.

---

## Funcionalidades

- Crear o cambiar contraseña maestra para acceso
- Iniciar sesión con la contraseña maestra
- Generar contraseñas con opciones personalizadas:
  - Longitud
  - Mayúsculas, minúsculas, números, símbolos
- Añadir contraseñas generadas a favoritos
- Descargar favoritos en archivo texto
- Vaciar lista de favoritos

---

## Cómo usar

### Requisitos

- Python 3.7+
- Flask (`pip install flask`)
- cryptography (`pip install cryptography`)

### Instalación

1. Clona o descarga este repositorio.
2. En la carpeta del proyecto, crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate   # Windows
   source venv/bin/activate  # Linux/Mac
