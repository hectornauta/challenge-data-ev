## Project Overview

El challenge fue desarrollado pensándolo de la siguiente manera y con las siguientes herramientas:
- Extraer datos (datos RAW o en bruto): valiéndome de la biblioteca *requests*
- Transformar (dato limpios y procesados): utilizando Pandas, trabajando con CSV para la lectura y parquet para la escritura
- Responder preguntas análiticas (información que responde las dudas del "negocio")
- - Mediante consultas: utilizando consultas SQL y guardándolo a una base de datos diferente, con DuckDB
- - Mediante una herramienta BI: a los resultados limpios, se responden las preguntas pero utilizando PowerBI y sus gráficos

## Fases
- Una fase de extracción de datos
- - Se escogió el archivo CSV ya que son los que suelen incluir algún que otro problema para procesarlos (a diferencia de algo más estructurado como JSON)
- - Sin embargo, el archivo JSON vemos que incluye más datos descriptivos (sobre columnas, por ejemplo)
- - Se incluye la posibilidad de realizar retries al origen de datos en caso de que el mismo falle, con un incremento exponencial de tiempo
- - La lectura de los tipos de datos se hacen asumiendo que todos son string y luego transformar manualmente las columnas específicas a sus tipos de datos adecuados, para evitar reconocmiento incorrecto de datos por parte de Pandas
- Una fase de transformación de datos
- - Se realiza una limpieza de columnas con valores nulos, pero no sobre ciertas columnas que dejarían el set de datos con solamente autos del  estado de Washington
- - Se realiza un renombre de las columnas sacando espacios, mayúsculas, símbolos, etc.
- - Se convierten los strings de tipo POINT(X,Y) al tipo de datos adecuado (latitud y longitud)
- - Se genera un archivo columnar parquet para poder ser consumido de forma rápida y ligera por PowerBI y para la fase de Analytics
- La fase de Analytics
- - Para integrar tanto Pandas como SQL (y que SQL no quede relegado a solamente un CREATE TABLE) las consultas se hacen con SQL sobre el dataframe obtenido de leer el parquet en el paso anterior
- - Los resultados de las 4 preguntas del challenge se exportan a una base de datos DuckDB (simplemente por razones de rapidez) en 4 tablas distintas
- - Para la tercer pregunta, se interpretó que el interés es saber cuáles son las regiones que agrupan más cantidad de registros (ordenados según cantidad de los mismos)
- La fase de visualización con PowerBI
- - Esta fase la hice tomando en cuenta a la otra interpretación que hice de las 4 preguntas del challenge: "Cómo veo estos datos en un dashboard"
- - Por eso, trabajé sobre los datos limpios y procesados (no sobre los resultados de las consultas de la fase de Analytics) para llegar al "mismo resultado"
- - Por ejemplo, utilizando latitud y longitud en un mapa es posible ver de forma más clara *dónde* se concentran los autos CAFV

## Desafíos
- En la fase de extracción surgió el clásico problema de errores al descargar el CSV, por lo cual se agregó la posibilidad de hacer retries con un delay incremental entre cada intento.
- En la fase de transformación, hubo que discriminar qué filas con nulos borrar y cuáles no. Porque algunos borrar todos los nulos dejaban el dataset confinado a solamente un estado. Por eso se decidió solamente borrar los nulos de una columna (la de ubicación)
- Se normalizaron los nombres de columnas. De forma similar a como lo requeriría una tabla de Athena
- En la fase de consultas, se buscó resolver utilizando SQL en vez de Pandas (simplemente para abarcar varios temas), así que fue cuestión de ver cuál era la forma ideal de integrar ambas cosas (dataframes y consultas con SQL puras) sin hacer complicar demás el problema
-  En el caso de PowerBI, el mayor desafío en realidad fue hacer la conversión previa (en transformación) de los strings POINT a Latitud y Longitud

## Posibles mejoras
- Realizar la orquestación de las tareas. Por ejemplo, utilizando AWS Step Functions con AWS Lambda (con varias funciones Lambda o una sola con distintos parámetros y versionado), sumándole programaciones con EventBridge.
- Separación de los datos en sus distintas etapas: por ejemplo en buckets de AWS S3 distintos (uno para los datos en bruto y otro para los transformados) y conectándolo a Athena para las consultas (aunque bueno, técnicamente también es internamente en otro bucket) de un BI como PowerBI o AWS Quick Suite.