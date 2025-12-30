# challenge-data-ev
Proyecto para un challenge de datos

## Prerrequisitos
- Tener instalado Python >=3.12.3

## Instrucciones

- Descargamos el repositorio de https://github.com/hectornauta/challenge-data-ev o bien lo clonamos
- Lo descargamos a una carpeta vacía de Windows, sobre la misma carpeta abrimos la consola de comandos y corremos ```python -m venv env```
- Activamos el entorno virtual con ```.\env\Scripts\activate``` //Esto puede variar en un entorno Linux
- Instalamos las dependencias con ```pip install -r requirements.txt```
- Ejecutamos el programa principal con ```python ./main.py```

## Configuración de PowerBI

- Al abrir el archivo **dashboard.pbix**, hacer clic en *Transform data* de la cinta principal de opciones
- En la sección derecha, en *Applied Steps* seleccionar *Source*
- Modificar la ruta allí asignada por la utilizada en su sistema para el archivo .pbix

```= Parquet.Document(File.Contents("C:\CARPETA_DESCARGADA\challenge-data-ev\data\processed\rows.parquet"), [Compression=null, LegacyColumnNameEncoding=false, MaxDepth=null])```

# Project Overview + Documentación

- Se encuentran en la carpeta ```docs/docs.md```