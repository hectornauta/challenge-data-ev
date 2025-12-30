import duckdb
import pandas as pd
from src.utils import prepare_folders
import os


def read_processed_data(processed_file_key: str) -> pd.DataFrame:
    """
    Lee un archivo parquet de la ruta especificada
    
    :param processed_file_key: ruta completa del archivo parquet
    :type processed_file_key: str
    :return: dataframe leído
    :rtype: DataFrame
    """
    print('Obteniendo el dataframe procesado')
    dataframe = pd.read_parquet(processed_file_key)
    return dataframe


def clean_db(analytics_key: str):
    # Limpiamos la DB por cada ejecución, solamente para que empecemos de cero siempre
    if os.path.exists(analytics_key):
        os.remove(analytics_key)
        print(f"Base '{analytics_key}' eliminada.")


def get_db_connection(analytics_key: str):
    conn = duckdb.connect(analytics_key, read_only=False)
    conn.sql("SHOW TABLES;").show()
    return conn


def execute_queries(dataframe: pd.DataFrame, conn):
    # Definimos la carpeta de queries y los nombres de los archivo
    sql_folder = 'sql/'
    sql_queries = [
        'vehicles_per_year.sql',
        'top_10_models.sql',
        'cafv_concentration.sql',
        'yoy_by_county.sql'
    ]
    # Iteramos por cada query
    for query_file in sql_queries:
        # Armamos el nombre completo y el de la tabla
        full_file_key = f"{sql_folder}{query_file}"
        print(f"Procesando: {full_file_key=}")
        table_name = str(query_file)
        table_name = table_name.replace('.sql', '')
        # Leemos el script y lo ejecutamos
        with open(full_file_key, 'r') as f:
            sql_script = f.read()
            print(f"El script es {sql_script=}")
            # Ejecutamos las queries sobre los dataframes
            result_query = duckdb.query(sql_script).df()
            print(result_query)
            # Mandamos el resultado a la DB
            conn.execute(query=f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM result_query")
            # conn.sql(f"SELECT * FROM {table_name}").show()


def show_db(conn):
    conn.sql("SHOW TABLES;").show()


def run_task():
    # Preparamos los directorios y nombres de archivos
    processed_folder = 'data/processed/'
    processed_file = 'rows.parquet'
    processed_file_key = f"{processed_folder}{processed_file}"
    analytics_folder = 'data/analytics/'
    analytics_file = 'analytics.db'
    analytics_key = f"{analytics_folder}{analytics_file}"
    prepare_folders(analytics_folder)
    # Leemos el archivo de datos limpios
    dataframe = read_processed_data(processed_file_key)
    # Preparamos la DB de cero
    # clean_db(analytics_key)
    # Obtenemos la conexión a la DB
    conn = get_db_connection(analytics_key)
    # Preparamos las consultas
    execute_queries(dataframe, conn)
    # Mostramos la base de datos final
    show_db(conn)


if __name__ == "__main__":
    run_task()
