"""
ingesta.py
----------
Fase 1 y 2 del Taller 3: Extracción desde una API pública y almacenamiento RAW en MongoDB.

- API usada: Rick and Morty API (https://rickandmortyapi.com) — endpoint /api/character
  No requiere llave y tiene más de 800 personajes repartidos en páginas de 20.
- Destino: base de datos `taller3_db`, colección `raw_data`.
- Cada personaje se guarda TAL CUAL llega de la API. Solo se agrega el campo `_id`
  con el mismo valor del `id` de la API, para que al ejecutar el script varias veces
  no se dupliquen documentos (se hace un upsert: si el _id ya existe, se reemplaza).

Uso:
    python ingesta.py
    (Para MongoDB Atlas: definir la variable de entorno MONGO_URI con la cadena de conexión)
"""

import os
import time

import requests
from pymongo import MongoClient, ReplaceOne

API_URL = "https://rickandmortyapi.com/api/character"
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "taller3_db"
COLLECTION_NAME = "raw_data"
MINIMO_REGISTROS = 100


def descargar_personajes(url_inicial: str) -> list[dict]:
    """Recorre todas las páginas de la API siguiendo el enlace `info.next`."""
    personajes = []
    url = url_inicial
    pagina = 1

    while url:
        respuesta = requests.get(url, timeout=30)
        respuesta.raise_for_status()  # lanza error si la API responde 4xx/5xx
        datos = respuesta.json()

        personajes.extend(datos["results"])
        print(f"Página {pagina}: {len(datos['results'])} personajes "
              f"(acumulado: {len(personajes)})")

        url = datos["info"]["next"]  # None cuando ya no hay más páginas
        pagina += 1
        time.sleep(0.2)  # pausa corta para no saturar la API

    return personajes


def guardar_en_mongo(personajes: list[dict]) -> None:
    """Guarda los documentos crudos usando el id de la API como _id (sin duplicados)."""
    cliente = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    cliente.admin.command("ping")  # verifica que MongoDB esté encendido
    coleccion = cliente[DB_NAME][COLLECTION_NAME]

    operaciones = []
    for personaje in personajes:
        documento = {"_id": personaje["id"], **personaje}  # JSON original + _id
        operaciones.append(
            ReplaceOne({"_id": documento["_id"]}, documento, upsert=True)
        )

    resultado = coleccion.bulk_write(operaciones)
    print("\nResumen de la carga en MongoDB:")
    print(f"  Documentos nuevos insertados: {resultado.upserted_count}")
    print(f"  Documentos ya existentes (reemplazados): {resultado.matched_count}")
    print(f"  Total en {DB_NAME}.{COLLECTION_NAME}: {coleccion.count_documents({})}")

    cliente.close()


def main() -> None:
    print(f"Descargando datos desde {API_URL} ...\n")
    personajes = descargar_personajes(API_URL)

    if len(personajes) < MINIMO_REGISTROS:
        raise ValueError(
            f"Solo se descargaron {len(personajes)} registros; se requieren {MINIMO_REGISTROS}."
        )

    print(f"\nTotal descargado: {len(personajes)} personajes")
    guardar_en_mongo(personajes)


if __name__ == "__main__":
    main()
