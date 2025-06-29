# Definición de los datos

## Origen de los datos

 Los datos fueron obtenidos desde [Kaggle](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia), y provienen del Guangzhou Women and Children’s Medical Center. Corresponden a radiografías de tórax (vista anteroposterior) tomadas como parte del cuidado clínico rutinario a pacientes pediátricos de 1 a 5 años. Las imágenes fueron evaluadas por al menos dos médicos expertos y curadas para eliminar imágenes de baja calidad. La licencia es CC BY 4.0. Más información: [Cell 2018](http://www.cell.com/cell/fulltext/S0092-8674(18)30154-5).

## Especificación de los scripts para la carga de datos

Los datos son obtenidos utilizando la API oficial de Kaggle, lo que permite su descarga automatizada directamente desde la plataforma. Posteriormente, se utiliza un script desarrollado en PySpark para procesar y transformar las imágenes y metadatos en un formato estructurado. Finalmente, los datos se almacenan en formato `.parquet` dentro de un entorno tipo Lakehouse, facilitando su análisis eficiente a gran escala. El script correspondiente se encuentra en la ruta raíz del proyecto: `scripts/data_acquisition`.

## Referencias a rutas o bases de datos origen y destino

Los datos de origen son descargados desde la plataforma de Kaggle mediante su API oficial y almacenados localmente en la ruta `src/Pneumonia_Detection/database`, donde se conservan las imágenes originales clasificadas. En esta misma ubicación se almacenan los datos procesados en formato `.parquet`, generados mediante PySpark. Esta estructura permite mantener centralizado el acceso tanto a los datos crudos como a los transformados, facilitando su trazabilidad, reutilización y análisis dentro de un entorno tipo Lakehouse.
La carpeta `bronze` contiene los datos crudos descargados desde Kaggle, mientras que la carpeta `silver` contiene los datos ya procesados.

### Rutas de origen de datos

- Los archivos de origen se almacenan localmente en la ruta `src/Pneumonia_Detection/database/bronze`, la cual contiene las imágenes descargadas desde Kaggle en su estructura original.

- Los datos están organizados en tres carpetas principales: `train`, `val` y `test`, cada una con dos subdirectorios correspondientes a las clases: `NORMAL` y `PNEUMONIA`. Las imágenes están en formato `.jpeg`.  
> src/Pneumonia_Detection/database/bronze/  
>├── train/  
>│   ├── NORMAL/  
>│   └── PNEUMONIA/  
>├── val/  
>│   ├── NORMAL/  
>│   └── PNEUMONIA/  
>└── test/  
>│   ├── NORMAL/  
>│   └── PNEUMONIA/  

- Durante la etapa de procesamiento, las imágenes son leídas y transformadas con PySpark. Se realizan tareas como verificación del formato, filtrado de archivos corruptos o vacíos, y asignación de etiquetas (0 para NORMAL y 1 para PNEUMONIA). Posteriormente, los datos se convierten a formato estructurado y se almacenan en `.parquet` bajo la ruta `src/Pneumonia_Detection/database/silver`, lo que permite su uso eficiente dentro del entorno analítico tipo Lakehouse.

### Base de datos de destino

- La base de datos de destino corresponde a un entorno tipo Lakehouse basado en archivos `.parquet`, almacenados localmente en la ruta `src/Pneumonia_Detection/database/silver`. Este enfoque permite combinar las ventajas del almacenamiento en data lakes (escalabilidad y bajo costo) con las capacidades de consulta estructurada de los data warehouses.

- Los datos procesados se almacenan como tablas en formato columnar `.parquet`, organizadas por particiones (`train`, `val`, `test`). Cada registro contiene los siguientes campos:

>| imagen_id | ruta_origen                                    | clase     | clase_codificada |
>|-----------|------------------------------------------------|-----------|------------------|
>| img001    | bronze/train/NORMAL/IM-0115-0001.jpeg          | NORMAL    | 0                |
>| img002    | bronze/train/PNEUMONIA/person02_bacteria.jpeg  | PNEUMONIA | 1                |

- La carga se realiza mediante un script en PySpark que recorre los directorios `train`, `val` y `test`, identifica las imágenes y asigna automáticamente su clase a partir del nombre del subdirectorio. Luego, se construye un DataFrame estructurado que se guarda en formato `.parquet` en la ruta `src/Pneumonia_Detection/database/silver`, permitiendo su posterior análisis y modelado mediante Spark SQL u otras herramientas compatibles.
