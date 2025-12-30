import requests
import os
from src.utils import prepare_folders
from requests.exceptions import RequestException
import time

URL_CSV = F"https://data.wa.gov/api/views/f6w7-q2d2/rows.csv?accessType=DOWNLOAD"


def csv_file_exists(file_path: str):
    """
    # TODO: borrar
    Revisa si el archivo indicado existe
    
    :param file_path: Archivo a revisar
    :type file_path: str
    """
    if os.path.isfile(file_path):
        print(f"Archivo ya descargado")
        return True
    else:
        return False


def download_csv(url: str, file_path: str):
    """
    Descarga un archivo csv y reintenta varias veces
    
    :param url: url del archivo a descargar
    :type url: str
    :param file_path: ruta completa donde se guardará el archivo si se descarga
    :type file_path: str
    """
    print(f"Preparando la descarga de archivos")
    # TODO Añadir retries
    max_retries = 6
    initial_time = 1
    response = None
    for attempt in range(max_retries):
        try:
            url_to_download = url
            # url_to_download = 'https://httpbin.org/status/502'
            print(f"Descargando {url_to_download}")
            response = requests.get(url_to_download)
            response.raise_for_status()
            break
        except RequestException as error:
            status = getattr(response, "status_code", None)
            if status is not None:
                print(f"Error de descarga ({status=}): {error=}")
            else:
                print(f"Error de conexión: {error=}")
            if attempt < max_retries - 1:
                wait_time = initial_time * (2 ** attempt)
                print(f"Reintentando en {wait_time}...")
                time.sleep(wait_time)
            else:
                break
    if response is None or not response.ok:
        print("Máxima cantidad de fallos")
        raise Exception('No se pudo descargar el archivo')
    else:
        with open(file_path, "wb") as file:
            file.write(response.content)
            print(f"Se descargó el archivo a {file_path}")


def run_task():
    # Definimos los nombres
    folder_path = 'data/raw/'
    file_name = 'rows.csv'
    file_path = f"{folder_path}{file_name}"
    # Preparamos las carpetas y subcarpetas
    prepare_folders(folder_path)

    always_download = False  # Sólo para tests
    if not csv_file_exists(file_path) or always_download:
        download_csv(URL_CSV, file_path)


if __name__ == "__main__":
    run_task()
