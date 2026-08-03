import sqlite3
import pandas as pd


def load_to_sqlite(df: pd.DataFrame, db_path: str, table_name: str) -> None:
    """
    Guarda un DataFrame en una tabla de una base de datos SQLite.
    Args:
        df: DataFrame a guardar
        db_path: ruta del archivo de base de datos (ej. "data/musica.db")
        table_name: nombre de la tabla donde se guardarán los datos
    """
    # TODO:

    conexion = sqlite3.connect(db_path)
    df.to_sql(table_name, conexion, if_exists="replace", index=False)
    conexion.close()


if __name__ == "__main__":
    from extract import get_artists_by_genre, get_artist_details, get_artist_metadata_musicbrainz
    from transform import build_combined_dataset, classify_emergent_artists
    
    artistas_basicos = get_artists_by_genre(132)  # tu ID de género (Pop)
    df_combinado = build_combined_dataset(artistas_basicos, get_artist_details, get_artist_metadata_musicbrainz)
    df_final = classify_emergent_artists(df_combinado)
    
    load_to_sqlite(df_final, "data/musica.db", "artistas_pop")
    print("Datos guardados exitosamente en la base de datos.")