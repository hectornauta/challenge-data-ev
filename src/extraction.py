import requests
import os
from utils import prepare_folders

URL_CSV = F"https://data.wa.gov/api/views/f6w7-q2d2/rows.csv?accessType=DOWNLOAD"


def download_csv(url: str):
    print(f"Preparando la descarga de archivos")
    # Definimos los nombres
    folder_path = 'data/raw/'
    prepare_folders(folder_path)
    file_name = 'rows.csv'
    file_path = f"{folder_path}{file_name}"

    # TODO Añadir retries
    try:
        print(f"Descargando {url}")
        response = requests.get(url)
        response.raise_for_status()  # Check if the download was successful

        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Se descargó el archivo a {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Ocurrió un error: {e}")


if __name__ == "__main__":
    download_csv(URL_CSV)
