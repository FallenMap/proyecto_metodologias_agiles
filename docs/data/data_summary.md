# Reporte de Datos

Este documento contiene los resultados del análisis exploratorio de datos del conjunto Chest X-Ray Images (Pneumonia), implementado como parte del procesamiento basada en Spark y Pandas.


## Resumen general de los datos

El conjunto de datos fue descargado desde [Kaggle - Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia) y contiene **5,863 imágenes de rayos X de tórax pediátricos**, en formato JPEG. Las imágenes están organizadas en tres carpetas: `train`, `val` y `test`, con subcarpetas para cada clase (`NORMAL` y `PNEUMONIA`).

Como parte del proceso de preprocesamiento, se diseñó un pipeline ETL que transforma las imágenes en una estructura tabular:

- Las imágenes se codifican en formato binario (`content`) y se almacenan como archivos Parquet (etapa *Silver*).
- Posteriormente, se extraen los pixeles, se convierten a escala de grises, se redimensionan a 128×128 píxeles y se normalizan (etapa *Gold*).
- Cada imagen procesada es representada como un vector de 16,384 valores entre 0 y 1.

Las columnas del conjunto procesado incluyen:

- `imagen_id`, `ruta_origen`, `clase`, `clase_codificada`, `split`
- `pixel_0` hasta `pixel_16383` (valores de los píxeles)


## Resumen de calidad de los datos

Durante el preprocesamiento se realizaron las siguientes verificaciones de calidad:

- Las imágenes ilegibles o con errores de lectura fueron descartadas.
- Se codificaron las etiquetas (`NORMAL`, `PNEUMONIA`) como valores numéricos (`0`, `1`).
- No se detectaron valores nulos ni duplicados tras la carga de los Parquet.
- Todas las imágenes fueron homogeneizadas a una dimensión fija de 128×128.
- Las imágenes se almacenaron separadas por clase y particionadas por split.

Esto permitió asegurar la trazabilidad, limpieza y consistencia de los datos desde su origen hasta su transformación final.
## Variable objetivo

La variable objetivo es **`clase`**, que indica la presencia o no de neumonía. Esta variable toma dos valores:

- `NORMAL`: pacientes sin diagnóstico de neumonía.
- `PNEUMONIA`: pacientes diagnosticados con neumonía.

Se graficó la distribución de clases para el conjunto de entrenamiento, evidenciando un **importante desbalance de clases**, con mayor proporción de imágenes etiquetadas como *PNEUMONIA*.

Este desbalance será relevante en fases posteriores de entrenamiento de modelos supervisados, ya que puede inducir sesgo predictivo si no se compensa adecuadamente.
## Variables individuales

Las variables individuales son los valores de los 16,384 píxeles de cada imagen, reescalados entre 0 y 1.

Se visualizó la distribución global de los valores de píxel en el conjunto de entrenamiento. La mayoría de los valores se concentra en rangos intermedios (0.5 a 0.7), con menor frecuencia de valores extremos cercanos a 0 o 1. Esto es coherente con la estructura típica de una radiografía en escala de grises.

Ademaás se verificó que no existen valores anómalos ni distorsiones por sobreexposición o subexposición, gracias al control de calidad previo.

## Ranking de variables

En esta sección se presenta un ranking de las variables más importantes para predecir la variable objetivo. Se utilizan técnicas como la correlación, el análisis de componentes principales (PCA) o la importancia de las variables en un modelo de aprendizaje automático.

## Relación entre variables explicativas y variable objetivo

Debido a la naturaleza visual de los datos, la relación entre variables (píxeles) y la clase objetivo no es directamente interpretable desde una matriz de correlación tradicional.

Sin embargo, se consideran las siguientes estrategias para analizar estas relaciones:

- Aplicar **t-SNE o UMAP** para proyectar los vectores de pixeles a 2D y observar agrupaciones por clase.
- Entrenar modelos clasificadores (SVM, CNN, etc.) y observar el comportamiento de separación entre clases.
- Explorar visualmente la diferencia entre imágenes promedio por clase (`NORMAL` vs `PNEUMONIA`).

Estas acciones permitirán cuantificar y visualizar las diferencias estructurales entre las clases en función de la información contenida en los píxeles.