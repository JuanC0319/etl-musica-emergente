import pandas as pd


def build_combined_dataset(artistas_basicos: list[dict], get_details_fn, get_metadata_fn) -> pd.DataFrame:
    """
    Combina datos de Deezer y MusicBrainz para cada artista en una sola tabla.
    
    Args:
        artistas_basicos: lista de artistas básicos (id, name) de Deezer
        get_details_fn: función para obtener detalles de Deezer (nb_fan, etc.)
        get_metadata_fn: función para obtener metadatos de MusicBrainz
    
    Returns:
        DataFrame con una fila por artista, combinando ambas fuentes
    """
    # TODO:
    lista_artistas = []
    for artista in artistas_basicos: 
        artistas_id = get_details_fn(artista["id"])
        artistas_info = get_metadata_fn(artista["name"])
        Detalles = {
            "Nombre" : artistas_id["name"],
            "Fan Base" : artistas_id["nb_fan"],
            "Pais" : artistas_info.get("country"),
            "Fecha formacion" : artistas_info.get("life-span", {}).get("begin")
        }
        lista_artistas.append(Detalles)
    df_artistas = pd.DataFrame(lista_artistas)
    return df_artistas


def classify_emergent_artists(df_artistas: pd.DataFrame, threshold_pct: float = 0.5) -> pd.DataFrame:
    """
    Clasifica artistas como 'emergente' según su nb_fan comparado con el Top N.
    
    Args:
        df: DataFrame con al menos las columnas 'name' y 'nb_fan'
        top_n: cuántos artistas considerar para la mediana (all)
        threshold_pct: porcentaje de la mediana que define el umbral (default 0.5)
    
    Returns:
        El mismo DataFrame, con una columna nueva 'es_emergente' (True/False)
    """
    # TODO:
    df_artistas_def = df_artistas.copy()
    df_ordenado = df_artistas.sort_values(by="Fan Base", ascending= False)
    mediana = df_ordenado['Fan Base'].median()
    umbral = mediana * threshold_pct
    df_artistas_def['es emergente'] = df_artistas_def['Fan Base'] < umbral
    return df_artistas_def

if __name__ == "__main__":
    from extract import get_artists_by_genre, get_artist_details, get_artist_metadata_musicbrainz
    
    artistas_basicos = get_artists_by_genre(132)
    df_combinado = build_combined_dataset(artistas_basicos, get_artist_details, get_artist_metadata_musicbrainz)
    df_final = classify_emergent_artists(df_combinado)
    
    print(df_final)
    print(f"\nArtistas emergentes encontrados: {df_final['es emergente'].sum()}")