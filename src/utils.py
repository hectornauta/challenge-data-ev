import os


def prepare_folders(folder_path: str):
    print(f"Preparando la carpeta {folder_path}")
    try:
        # Creamos las carpetas si no existen
        os.makedirs(folder_path, exist_ok=True)
        print(f"Directorios '{folder_path}' listos")
    except OSError as e:
        print(f"Error al crear directorios: {e}")