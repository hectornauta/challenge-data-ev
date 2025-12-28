import requests
import os

URL_CSV = F"https://data.wa.gov/api/views/f6w7-q2d2/rows.csv?accessType=DOWNLOAD"


def prepare_folders(folder_path: str):
    print(f"Preparando la carpeta {folder_path}")
    try:
        # Creamos las carpetas si no existen
        os.makedirs(folder_path, exist_ok=True)
        print(f"Directorios '{folder_path}' listos")
    except OSError as e:
        print(f"Error al crear directorios: {e}")


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
