# TrackPro API & Dashboard

TrackPro es una plataforma Fullstack de trazabilidad logística que desarrollé para consolidar mis conocimientos en desarrollo Backend moderno y diseño Frontend sin frameworks. 

El sistema permite rastrear paquetes en tiempo real a través de un portal público, mientras provee un dashboard administrativo protegido para gestionar los estados de envío mediante una API RESTful.

## Arquitectura y Tecnologías

He mantenido la arquitectura lo más limpia y modular posible, evitando dependencias innecesarias cuando las herramientas nativas son suficientes.

**Backend:**
- **FastAPI**: Elegido por su velocidad y soporte nativo para asincronismo y validación de tipos (Pydantic).
- **SQLModel / SQLAlchemy**: ORM para la gestión de la base de datos y validación de esquemas.
- **PostgreSQL**: Motor de base de datos relacional (desplegado vía Docker).
- **Seguridad**: JWT (JSON Web Tokens) para manejo de sesiones y `bcrypt` crudo para el hashing de contraseñas.

**Frontend:**
- **Vanilla JS, HTML5, CSS3**: Decidí no utilizar frameworks (como React o Tailwind) para demostrar dominio puro del DOM y CSS moderno (implementando un patrón Glassmorphism y Dark Mode desde cero).
- Consumo asíncrono de la API mediante Fetch.

## Instalación y Ejecución Local

Para levantar el entorno local, asegúrate de tener Docker y Python 3.10+ instalados.

1. **Clonar y preparar entorno:**
   ```bash
   git clone <URL_DE_TU_REPOSITORIO>
   cd logistics_api
   python -m venv venv
   source venv/bin/activate  # En Windows usa: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Levantar base de datos:**
   ```bash
   docker-compose up -d
   ```

3. **Iniciar servidor:**
   ```bash
   uvicorn main:app --reload
   ```

4. **Acceder a la aplicación:**
   Abre el archivo `frontend/index.html` en tu navegador, o consulta la documentación interactiva de la API en `http://localhost:8000/docs`.

## Retos Técnicos Superados

Durante el desarrollo, me enfrenté a un problema interesante relacionado con la seguridad. Inicialmente implementé `passlib` para manejar el cifrado de contraseñas. Sin embargo, al probar el registro de usuarios, la API devolvió un Error 500 de servidor.

Al debugear el traceback y analizar los logs, descubrí que `passlib` tiene un bug de compatibilidad conocido con las versiones recientes de `bcrypt` (4.0+) en Python 3.12, ya que falla en la validación interna de los hashes. 

En lugar de hacer un *downgrade* a una versión insegura o antigua de `bcrypt` para complacer a la librería, refactoricé el módulo de autenticación (`auth.py`) para deshacerme de `passlib` y consumir la API moderna de `bcrypt` de forma directa (`bcrypt.hashpw` y `bcrypt.checkpw`). Esto no solo resolvió el problema de raíz, sino que eliminó una dependencia obsoleta haciendo el sistema más ligero y fácil de mantener.

## Próximos Pasos (Roadmap)
- Implementar pruebas unitarias en Python.
- Dockerizar la aplicación completa (Backend + Frontend) para producción.
