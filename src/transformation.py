import pandas as pd
from utils import prepare_folders


def read_ev_csv(file_key: str)->pd.DataFrame:
    print('Leyendo csv')
    dataframe = pd.read_csv(
        file_key,
        dtype=str
    )
    return dataframe


def clean_dataframe(dataframe: pd.DataFrame)->pd.DataFrame:
    print('Limpiando dataframe')
    dataframe['electric_range'] = dataframe['electric_range'].astype(float)
    # cols_with_empty_strings = dataframe.columns[dataframe.eq('').any()]
    # print("Columnas con strings vacíos")
    # print(cols_with_empty_strings)
    # Limpiamos los nulos
    cols_with_nulls = dataframe.columns[dataframe.isnull().any()]
    print("Columnas con nulos")
    print(cols_with_nulls)
    # print(F"Antes de borrar nulos: {len(dataframe)=}")
    """
    De momento pasamos por alto los nulos de
        - 2020 Census Tract porque parece ser algo de un censo
        - Electric Utility porque es algo de una compañía eléctrica
        - Legistlative District porque es algo exclusivo de WA
    """
    dataframe = dataframe.dropna(subset=['vehicle_location'])
    # print(F"Luego de borrar nulos: {len(dataframe)=}")
    return dataframe


def normalize_names(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe.columns = dataframe.columns.str.strip()
    dataframe.columns = dataframe.columns.str.lower().str.replace(" ", "_")
    dataframe.columns = dataframe.columns.str.replace(r'[^a-z0-9_]+', '', regex=True)
    dataframe.columns = dataframe.columns.str.strip('_')
    dataframe = dataframe.rename(columns={
        'vin_110': 'vin',
        'clean_alternative_fuel_vehicle_cafv_eligibility': 'cafv_eligibility'
    })
    return dataframe


def transform_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    # Ajustamos los datos geográficos
    dataframe['location'] = dataframe['vehicle_location'].str.replace('POINT (', '').str.replace(')', '').str.split(' ')
    dataframe['longitude'] = dataframe['location'].str[0].astype(float)
    dataframe['latitude'] = dataframe['location'].str[1].astype(float)
    dataframe['latitude'] = dataframe['location'].str[1].astype(float)
    # Ajustamos esto para tener como formato fecha
    dataframe['date_model'] = pd.to_datetime(dataframe['model_year'].astype(str) + '-01-01')
    dataframe = dataframe.drop(columns=['location'])
    print(f"Nuevos nombres de columnas {dataframe.columns=}")
    return dataframe


def save_dataframe_ev(dataframe: pd.DataFrame, file_key: str):
    # Guardamos como datos limpios
    dataframe.to_parquet(
        processed_file_key,
        index=False
    )


if __name__ == "__main__":
    raw_folder = 'data/raw/'
    raw_file = 'rows.csv'
    raw_file_key = f"{raw_folder}{raw_file}"
    processed_folder = 'data/processed/'
    processed_file = 'rows.parquet'
    processed_file_key = f"{processed_folder}{processed_file}"
    prepare_folders(processed_folder)

    dataframe_ev = read_ev_csv(raw_file_key)
    dataframe_ev = normalize_names(dataframe_ev)
    dataframe_ev = clean_dataframe(dataframe_ev)
    dataframe_ev = transform_dataframe(dataframe_ev)
    save_dataframe_ev(dataframe_ev, processed_file_key)
    print(f"{dataframe_ev=}")