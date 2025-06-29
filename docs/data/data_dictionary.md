# Diccionario de datos

## Base de datos Bronze: Datos crudos (imágenes originales descargadas)

Corresponde a los archivos originales en formato `.jpeg` descargados desde Kaggle, organizados en carpetas por conjunto (`train`, `val`, `test`) y clase (`NORMAL`, `PNEUMONIA`). Estas imágenes fueron tomadas del Guangzhou Women and Children’s Medical Center, y representan radiografías de tórax pediátricas utilizadas para el diagnóstico de neumonía.

| Variable         | Descripción                                                           | Tipo de dato | Rango/Valores posibles                           | Fuente de datos                                                  |
|------------------|-----------------------------------------------------------------------|--------------|--------------------------------------------------|------------------------------------------------------------------|
| nombre_archivo   | Nombre original del archivo de imagen                                 | string       | IM-0115-0001.jpeg, person02_bacteria.jpeg, etc.  | Descarga directa desde Kaggle                                   |
| ruta_archivo     | Ruta relativa dentro del almacenamiento local del conjunto de datos                                      | string       | train/NORMAL/..., test/PNEUMONIA/..., val/PNEUMONIA/             | Estructura de carpetas de Kaggle                                |
| clase            | Categoría de la imagen según diagnóstico clínico                      | string       | NORMAL, PNEUMONIA                                | Asignada por médicos especialistas según diagnóstico             |
| conjunto         | División del conjunto de datos                                        | string       | train, val, test                                 | Determinada por los autores del dataset                         |
| formato_imagen   | Formato del archivo de imagen                                         | string       | jpeg                                             | Estándar en todos los archivos del dataset                      |

## Base de datos Silver: Datos procesados en formato `.parquet`

Contiene los metadatos asociados a las imágenes de rayos X procesadas, que han sido transformadas desde su forma original (.jpeg) en Kaggle hacia un formato estructurado optimizado para análisis en entornos tipo Lakehouse.

| Variable         | Descripción                                                  | Tipo de dato | Rango/Valores posibles         | Fuente de datos                                                  |
|------------------|--------------------------------------------------------------|--------------|-------------------------------|------------------------------------------------------------------|
| imagen_id        | Identificador único generado para cada imagen                | string       | img001, img002, ...            | Generado automáticamente en el script PySpark                   |
| ruta_origen      | Ruta relativa al archivo de imagen original                  | string       | bronze/train/NORMAL/IM-0001.jpeg | Directorios locales tras descarga desde Kaggle                  |
| clase            | Etiqueta textual de la categoría de la imagen                | string       | NORMAL, PNEUMONIA              | Nombre del subdirectorio de origen                              |
| clase_codificada | Etiqueta numérica codificada para la clase de la imagen      | integer      | 0 = NORMAL, 1 = PNEUMONIA      | Asignada automáticamente en el proceso de transformación PySpark |
| particion        | Conjunto de datos al que pertenece la imagen                 | string       | train, val, test               | Carpeta de origen del conjunto (entrenamiento, validación, test)|
