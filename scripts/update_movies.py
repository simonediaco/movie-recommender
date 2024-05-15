import pandas as pd
import requests
import os
from tqdm import tqdm
import time

# Percorso del file CSV originale
file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'movies.csv')

# Carica il file CSV originale
movies_df = pd.read_csv(file_path).head(2)


# Funzione per ottenere i dettagli del film dall'API OMDb
def get_movie_details(title):
    api_key = '168e42af'  # La tua nuova chiave API
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    response = requests.get(url)

    # Controlla se la richiesta ha avuto successo
    if response.status_code == 401:
        raise ValueError("Errore 401: API key non autorizzata. Verifica la tua API key.")
    if response.status_code != 200:
        return {}

    try:
        data = response.json()
    except ValueError:
        return {}

    return data


# Rimuovi l'anno dal titolo, se presente
movies_df['cleanTitle'] = movies_df['title'].str.replace(r'\(\d{4}\)', '').str.strip()

# Inizializza un DataFrame per memorizzare i risultati
omdb_fields = ['Title', 'Year', 'Rated', 'Released', 'Runtime', 'Genre', 'Director', 'Writer', 'Actors', 'Plot',
               'Language', 'Country', 'Awards', 'Poster', 'Metascore', 'imdbRating', 'imdbVotes', 'imdbID', 'Type',
               'DVD', 'BoxOffice', 'Production', 'Website', 'Response']
results_df = pd.DataFrame(columns=omdb_fields)

# Applica la funzione per ottenere i dettagli del film con tqdm per la barra di progresso
for index, row in tqdm(movies_df.iterrows(), total=movies_df.shape[0]):
    try:
        details = get_movie_details(row['cleanTitle'])
    except ValueError as e:
        print(e)
        break

    # Crea un DataFrame temporaneo per i dettagli ottenuti
    temp_df = pd.DataFrame([details], columns=omdb_fields)

    # Concatena il DataFrame temporaneo con il DataFrame dei risultati
    results_df = pd.concat([results_df, temp_df], ignore_index=True)

    # Attendi un secondo per evitare di sovraccaricare l'API
    time.sleep(1)

# Percorso per salvare il file CSV aggiornato
output_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'omdb_movies.csv')

# Salva il file CSV aggiornato
results_df.to_csv(output_file_path, index=False)

print(f"File aggiornato salvato in: {output_file_path}")
