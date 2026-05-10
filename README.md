# TrackPro by NexLogix 📦

Una plataforma completa (API RESTful + Frontend Web) para la gestión y trazabilidad de paquetes logísticos. 

## 🚀 Características Principales

### Backend (API)
- **Construcción Robusta:** Desarrollada con Python, FastAPI, SQLModel y PostgreSQL.
- **Seguridad JWT:** Autenticación de administradores con JSON Web Tokens y contraseñas encriptadas con Bcrypt.
- **Historial Automatizado:** Trazabilidad inmutable de cada cambio de estado o ubicación de los paquetes.
- **CORS Habilitado:** API configurada para aceptar peticiones web cruzadas de forma segura.

### Frontend (Web Dashboard)
- **Diseño Premium:** Interfaz de usuario moderna estilo *Glassmorphism* (Cristal), modo oscuro y animaciones fluidas, construida con Vanilla HTML/CSS/JS.
- **Rastreo Público:** Buscador de guías en tiempo real para clientes finales, mostrando una línea de tiempo del paquete (sin requerir contraseña).
- **Panel Administrativo:** Tablero privado protegido por inicio de sesión, que permite visualizar todos los paquetes y actualizar sus estados y ubicaciones fácilmente mediante un Modal interactivo.

## 🛠️ Tecnologías Utilizadas
- **Backend:** Python 3.10+, FastAPI, SQLModel, PostgreSQL, PyJWT, Bcrypt, Uvicorn, Docker.
- **Frontend:** HTML5, CSS3 (Vanilla), JavaScript (ES6+), Fetch API.

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
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la API:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Abrir la Página Web (Frontend):**
   No es necesario un servidor web adicional para el frontend. Simplemente abre el archivo ubicado en `frontend/index.html` haciendo doble clic en él, o ejecútalo desde tu terminal de Windows usando:
   ```cmd
   start frontend\index.html
   ```

## 🔐 Uso de la Plataforma

- **Como Cliente:** En la página web principal, ingresa cualquier número de guía válido para ver su historial en vivo a través del buscador.
- **Como Administrador:** 
  1. Si no tienes un usuario creado, créalo primero directamente en la documentación de la API en [http://localhost:8000/docs](http://localhost:8000/docs) (ruta `POST /usuarios/`).
  2. En la página web, ve a la pestaña "Acceso Admin" e inicia sesión con tus credenciales.
  3. Gestiona y actualiza los paquetes directamente desde la tabla visual con el Modal interactivo.

---
Desarrollado como proyecto Fullstack Integral.
