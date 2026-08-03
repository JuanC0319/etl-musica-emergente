🇪🇸 Español | [🇬🇧 English](README.md)

# ETL Música Emergente

## Descripción
Pipeline de ETL (Extracción, Transformación y Carga) que identifica y analiza artistas emergentes dentro del Top 50 de música pop a nivel latinoamericano, combinando datos de popularidad con metadatos enriquecidos de artistas.

## Arquitectura
- **Extracción**: consumo de las APIs públicas de Deezer y MusicBrainz.
- **Transformación**: combinación de ambas fuentes en un DataFrame de pandas, y clasificación de cada artista como "emergente" o "no emergente" según su métrica de popularidad.
- **Carga**: almacenamiento de los datos transformados en una base de datos SQLite.

## Tecnologías utilizadas
- Python 3.12
- pandas
- requests
- SQLite

## Criterio de "artista emergente"
Un artista se clasifica como emergente si su número de fans (`nb_fan`) es menor al 50% de la mediana del fan base de todo el Top 50 analizado.

Inicialmente, el criterio se definió como el 50% del **promedio** del fan base del Top 10. Sin embargo, la presencia de outliers significativos en ese Top 10 (artistas con decenas de millones de fans) distorsionaba la métrica, clasificando como "emergentes" a artistas que en realidad ya están consolidados en la industria. Por esta razón, se ajustó el criterio para usar la **mediana** de todo el dataset, una medida más robusta ante valores extremos.

## Cómo ejecutar el proyecto
```bash
git clone https://github.com/JuanC0319/etl-musica-emergente.git
cd etl-musica-emergente
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Crear archivo .env con la variable MUSICBRAINZ_USER_AGENT
python3 src/load.py
```

## Estructura del proyecto
.
├── README.md
├── README.es.md
├── config
│ └── settings.py
├── data
│ └── musica.db
├── logs
├── requirements.txt
├── src
│ ├── init.py
│ ├── extract.py
│ ├── load.py
│ ├── main.py
│ └── transform.py
└── tests

## Aprendizajes y decisiones técnicas
Inicialmente se planteó trabajar con la API de Spotify, pero sus recientes restricciones de acceso para aplicaciones nuevas limitaban justo los datos de popularidad necesarios para el análisis. Se evaluó Last.fm como alternativa, pero su plataforma de registro presentaba fallas persistentes que impedían generar una API key. Finalmente se optó por la API de Deezer, que ofrece información equivalente sin fricciones técnicas.

Adicionalmente, debido al rate limiting de MusicBrainz, fue necesario introducir una pausa entre peticiones para evitar respuestas fallidas durante la extracción. También se utilizó el método `.get()` de Python en lugar de acceso directo por claves, para manejar de forma segura los casos en que la API no devolvía toda la información esperada.