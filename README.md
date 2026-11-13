# Taller 3 — APIs Públicas, MongoDB y EDA

**Curso:** Bases de Datos para Ciencia de Datos — Docente: Miguel Ramos García
**Estudiante:** Ingrid Yohana Orrego García 

## Descripción del proyecto

Este proyecto simula un flujo real de Ciencia de Datos en tres fases:

1. **Extracción:** se consumen los datos de una API pública.
2. **Almacenamiento RAW:** los datos se guardan sin modificar en MongoDB.
3. **Procesamiento y EDA:** se leen los datos desde MongoDB, se seleccionan variables clave y se hace un análisis exploratorio con estadísticas y gráficos.

## API utilizada

[Rick and Morty API](https://rickandmortyapi.com) — endpoint `https://rickandmortyapi.com/api/character`

- Gratuita y sin llave (API key).
- Contiene más de 800 personajes, entregados en páginas de 20 registros. El script recorre todas las páginas siguiendo el campo `info.next`.
- Cada personaje incluye nombre, estado, especie, género, origen, ubicación y la lista de episodios en que aparece.

## Estructura del repositorio

```
├── README.md          # Este archivo
├── requirements.txt   # Librerías necesarias
├── ingesta.py         # Extracción desde la API y carga RAW en MongoDB
├── analisis.ipynb     # Notebook con la selección de variables y el EDA
└── .gitignore         # Archivos excluidos del repositorio
```

## Almacenamiento en MongoDB

- Base de datos: `taller3_db`
- Colección: `raw_data`
- Cada documento es el JSON original del personaje. Se usa el `id` de la API como `_id`, y la carga se hace con *upsert*, por lo que ejecutar `ingesta.py` varias veces **no duplica** documentos.

## Requisitos previos

- Python 3.10 o superior
- MongoDB Community Server (local) con MongoDB Compass, o un clúster de MongoDB Atlas
- Git

## Cómo ejecutarlo

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
   cd TU_REPOSITORIO
   ```
2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```
3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Verificar que MongoDB esté corriendo en `mongodb://localhost:27017/`.
   *Si usas Atlas, define la variable de entorno `MONGO_URI` con tu cadena de conexión antes de ejecutar el script.*
5. Ejecutar la ingesta:
   ```bash
   python ingesta.py
   ```
6. Abrir el notebook y ejecutar todas las celdas:
   ```bash
   jupyter notebook analisis.ipynb
   ```

## Variables seleccionadas para el análisis

| Variable | Descripción |
|---|---|
| `nombre` | Nombre del personaje |
| `estado` | Alive, Dead o unknown |
| `especie` | Especie del personaje |
| `genero` | Male, Female, Genderless o unknown |
| `origen` | Lugar de origen |
| `ubicacion` | Última ubicación conocida |
| `num_episodios` | Cantidad de episodios en que aparece (derivada de la lista `episode`) |

## Contenido del análisis (analisis.ipynb)

- Inspección básica: `head()`, `info()` y verificación de nulos y valores `"unknown"`.
- Cinco insights numéricos: distribución por estado, personaje con más episodios, promedio de episodios por personaje, especie más común y origen más frecuente.
- Tres gráficos: torta por género, barras con el top 10 de especies e histograma del número de episodios por personaje.
