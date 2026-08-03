[🇪🇸 Español](README.es.md) | 🇬🇧 English

# Emerging Artists ETL

## Description
An ETL (Extract, Transform, Load) pipeline that identifies and analyzes emerging artists within the Latin American Pop Top 50, combining popularity metrics with enriched artist metadata.

## Architecture
- **Extract**: data is pulled from the public Deezer and MusicBrainz APIs.
- **Transform**: both sources are combined into a pandas DataFrame, and each artist is classified as "emerging" or "not emerging" based on a popularity metric.
- **Load**: the transformed data is stored in a SQLite database.

## Tech stack
- Python 3.12
- pandas
- requests
- SQLite

## "Emerging artist" criteria
An artist is classified as emerging if their fan count (`nb_fan`) is below 50% of the median fan base across the entire Top 50 dataset.

The criteria was initially defined as 50% of the **average** fan base of the Top 10. However, significant outliers within that Top 10 (artists with tens of millions of fans) skewed the metric, causing already well-established artists to be misclassified as "emerging." As a result, the criteria was adjusted to use the **median** of the full dataset instead, a measure more resistant to extreme values.

## How to run the project
```bash
git clone https://github.com/JuanC0319/etl-musica-emergente.git
cd etl-musica-emergente
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Create a .env file with the MUSICBRAINZ_USER_AGENT variable
python3 src/load.py
```

## Project structure

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

## Learnings and technical decisions
The project initially aimed to use the Spotify API, but its recent access restrictions for new applications limited exactly the popularity data needed for this analysis. Last.fm was evaluated as an alternative, but its registration platform had persistent issues that prevented generating an API key. The Deezer API was ultimately chosen, providing equivalent data without technical friction.

Additionally, due to MusicBrainz's rate limiting, a delay between requests was introduced to prevent failed responses during extraction. Python's `.get()` method was also used instead of direct key access, to safely handle cases where the API did not return all expected fields.