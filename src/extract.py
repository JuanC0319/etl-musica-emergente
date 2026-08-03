import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

MUSICBRAINZ_USER_AGENT = os.getenv("MUSICBRAINZ_USER_AGENT")

DEEZER_BASE_URL = "https://api.deezer.com"


def get_artists_by_genre(genre_id: int) -> list[dict]:
    """
    Obtiene la lista básica de artistas de un género desde Deezer.
    
    Args:
        genre_id: ID numérico del género en Deezer
    
    Returns:
        Lista de diccionarios con id y name de cada artista
    """
    # TODO:
    url_genre = f"{DEEZER_BASE_URL}/genre/{genre_id}/artists"
    listado = requests.get(url_genre)
    datosg = listado.json()
    lista_artistas = datosg["data"]
    return lista_artistas


def get_artist_details(artist_id: int) -> dict:
    """
    Obtiene los detalles completos de un artista específico (incluye nb_fan).
    
    Args:
        artist_id: ID del artista en Deezer
    
    Returns:
        Diccionario con los datos completos del artista
    """
    # TODO:
    url_artist =f"{DEEZER_BASE_URL}/artist/{artist_id}"
    artista = requests.get(url_artist)
    datosar = artista.json()
    return datosar


def get_artist_metadata_musicbrainz(artist_name: str) -> dict:
    """
    Ya la tenías planteada de antes - búsqueda en MusicBrainz.
    (esta función no cambia, sigue igual a como la diseñamos)
    """
    # TODO: 
    URL_BASE = f"https://musicbrainz.org/ws/2/artist"
    parametros = {
        "query":artist_name,
        "fmt" : "json"
    }
    artista_music = requests.get (URL_BASE, params=parametros, headers={"User-Agent": MUSICBRAINZ_USER_AGENT})
    datos_artista = artista_music.json()
    lista_artistas = datos_artista.get("artists", [])

    time.sleep(1)

    if lista_artistas:
        return lista_artistas[0]  # el primer resultado, el más relevante
    else:
        return {}
    

if __name__ == "__main__":
    artistas_basicos = get_artists_by_genre(132)
    print(f"Encontrados {len(artistas_basicos)} artistas")
    
    if artistas_basicos:
        primer_artista = artistas_basicos[0]
        detalles = get_artist_details(primer_artista["id"])
        print(f"Deezer - nb_fan: {detalles['nb_fan']}")
        
        metadata = get_artist_metadata_musicbrainz(primer_artista["name"])
        print(f"MusicBrainz - país: {metadata.get('country')}, inicio: {metadata.get('life-span', {}).get('begin')}")