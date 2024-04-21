# SEASOS - Backend

---

## Descripción del Proyecto

SEASOS es una aplicación diseñada para proporcionar información sobre especies marítimas en peligro de extinción. El backend está desarrollado utilizando Python y Flask, con MongoDB como base de datos. El objetivo principal del backend es ofrecer una API REST que será consumida por una interfaz frontend desarrollada en React, hospedada en Vercel.

---

## Instalación y Ejecución

Para configurar y ejecutar el backend de SEASOS, siga estos pasos:

1. **Clonar el Repositorio**
   ```bash
   git clone https://github.com/tu_usuario/seasos-backend.git
   cd seasos-backend
   ```
2. **Instalar Dependencias**
Asegúrese de tener Python y pip instalados en su sistema. Luego, cree y active un entorno virtual:
   ```bash
   python -m venv venv
   \venv\Scripts\bin\activate   # Para Windows
   source venv/bin/activate      # Para MacOS/Linux
   pip install -r requirements.txt
   ```
3. **Configurar MongoDB**
   Asegúrese de tener una instancia de MongoDB en ejecución. Puede configurar las credenciales y la URL de conexión en el archivo de configuración (.env) del proyecto. 
   # En este caso ya se tiene una instancia en el .env que es a nuestra base de animales (como solo se usara para desarrollo y calificación se espera el buen uso de esta misma)
4. **Ejecutar el backend**
   Para ejecutar el backend se deberá levantar el entorno virtual (por lo tanto es necesario hacer la lista de pasos en orden)
    ```bash
    python app.py
    ```
## Endpoints API

Una vez que el backend esté en funcionamiento, puede interactuar con la API REST utilizando los siguientes endpoints:

- `GET /api/species`: Obtener la lista de especies marítimas en peligro de extinción.
- `GET /api/species/{id}`: Obtener detalles de una especie específica por su ID.
- `POST /api/species`: Agregar una nueva especie a la base de datos.
- `PUT /api/species/{id}`: Actualizar los detalles de una especie existente.
- `DELETE /api/species/{id}`: Eliminar una especie de la base de datos.

### Ejemplos de Uso

#### Obtener la lista de especies

```http
GET /get/animals
POST /post/animals
Content-Type: application/json

{
  "nombre": "Especie Nueva", # Nombre del animal
  "cientifico": "En Peligro", # Nombre cientifico del animal
  "region ": "Nicaragua", # Region donde se encuentra el animal
  "latitud ": "32.41", # Latitud de donde se encuentra esa region (Mayormente punto centrico o aproximado donde este el animal)
  "longitud ": "98.12", # Longitud de donde se encuentra esa region (Mayormente punto centrico o aproximado donde este el animal)
  "img ": "https://www.ejemplo.com/imagen.jpg" # Enlace de imagen del animal
}

PUT /update/animals/<id> # ObjectId del registro en mongo.
Content-Type: application/json

{
  "nombre": "Especie Nueva", # Nombre del animal
  "cientifico": "En Peligro", # Nombre cientifico del animal
  "region ": "Nicaragua", # Region donde se encuentra el animal
  "latitud ": "32.41", # Latitud de donde se encuentra esa region (Mayormente punto centrico o aproximado donde este el animal)
  "longitud ": "98.12", # Longitud de donde se encuentra esa region (Mayormente punto centrico o aproximado donde este el animal)
  "img ": "https://www.ejemplo.com/imagen.jpg" # Enlace de imagen del animal
  "status": True  # Este campo se utilizara para aprobar solicitudes de animales brindadas usuarios.
}

DELETE /delete/animals/<id> # ObjectId del registro en mongo.
