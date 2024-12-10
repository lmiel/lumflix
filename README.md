# LUMFLIX
Link web: lumflix.vercel.app

Link GitHub: https://github.com/lmiel/lumflix.git

Lumflix es una aplicación de streaming basada en Django que permite explorar películas y series populares con una interfaz moderna y responsiva gracias a Bootstrap.

## Características

- Navegación por películas y series populares.
- Información detallada de cada título.
- Interfaz interactiva y amigable.

## Tecnologías

- **Backend**: Django 4.x
- **Frontend**: HTML, CSS, Bootstrap 5
- **Base de datos**: PostgreSQL (NeonDB)
- **API externa**: [TMDb API](https://www.themoviedb.org/)

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/lumflix.git
   cd lumflix ```
  
2. Instala las dependencias:
    ```bash
   pip install -r requirements.txt ```

3. Configura la clave API en un archivo .env:
    ```bash
    TMDB_API_KEY=tu_clave_api_aqui
    ```

5. Configura PostgreSQL en settings.py o en tu archivo .env.
6. Realiza las migraciones y arranca el servidor:
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```
  
6. Accede a la aplicación en: http://127.0.0.1:8000

Este formato es más conciso y directo. Puedes adaptarlo según lo que consideres esencial para tu proyecto. 😊

## Créditos

Lumflix fue desarrollado como parte de un proyecto académico por Lmiel. Agradecimientos especiales a TMDb por su API.
