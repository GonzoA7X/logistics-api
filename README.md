# API de Trazabilidad Logística 📦

Una API RESTful robusta para la gestión y trazabilidad de paquetes logísticos. Construida con Python, FastAPI, SQLModel, PostgreSQL y protegida con JSON Web Tokens (JWT).

## 🚀 Características
- **CRUD Completo:** Creación, lectura, actualización y eliminación de paquetes.
- **Validación Estricta:** Uso de Enums para estados de envío (`PENDIENTE`, `EN_TRANSITO`, `ENTREGADO`, `CANCELADO`).
- **Historial de Movimientos:** Trazabilidad automática de cada cambio de estado o ubicación de un paquete.
- **Seguridad:** Autenticación de usuarios y protección de rutas mediante tokens JWT y contraseñas encriptadas con Bcrypt.
- **Dockerizado:** Base de datos PostgreSQL lista para usar con Docker Compose.

## 🛠️ Tecnologías
- Python 3.10+
- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- PostgreSQL
- PyJWT & Bcrypt
- Docker

## ⚙️ Instalación y Uso Local

1. **Clonar el repositorio:**
   ```bash
   git clone <URL_DE_TU_REPOSITORIO>
   cd logistics_api
   ```

2. **Levantar la Base de Datos:**
   Asegúrate de tener Docker abierto y ejecuta:
   ```bash
   docker-compose up -d
   ```

3. **Instalar Dependencias:**
   Se recomienda usar un entorno virtual:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la API:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Probar la API:**
   Abre tu navegador y ve a: [http://localhost:8000/docs](http://localhost:8000/docs) para ver la documentación interactiva de Swagger UI.

## 🔐 Autenticación
Para probar los endpoints protegidos en Swagger, primero debes:
1. Crear un usuario en la ruta `POST /usuarios/`.
2. Hacer clic en el botón verde **"Authorize"** en la esquina superior derecha.
3. Iniciar sesión con tus credenciales para obtener un Token JWT temporal.
