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
    dataframe['Electric Range'] = dataframe['Electric Range'].astype(float)
    dataframe = dataframe.rename(columns={
        'VIN (1-10)': 'VIN'
    })
    return dataframe


def transform_dataframe(dataframe: pd.DataFrame)->pd.DataFrame:
    # Ajustamos los datos geográficos
    dataframe['Location'] = dataframe['Vehicle Location'].str.replace('POINT (', '').str.replace(')', '').str.split(' ')
    dataframe['Longitude'] = dataframe['Location'].str[0].astype(float)
    dataframe['Latitude'] = dataframe['Location'].str[1].astype(float)
    dataframe['Latitude'] = dataframe['Location'].str[1].astype(float)
    # Ajustamos esto para tener como formato fecha
    dataframe['Date Model'] = pd.to_datetime(dataframe['Model Year'].astype(str) + '-01-01')
    dataframe = dataframe.drop(columns=['Location'])
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
    dataframe_ev = clean_dataframe(dataframe_ev)
    dataframe_ev = transform_dataframe(dataframe_ev)
    save_dataframe_ev(dataframe_ev, processed_file_key)
    print(f"{dataframe_ev=}")