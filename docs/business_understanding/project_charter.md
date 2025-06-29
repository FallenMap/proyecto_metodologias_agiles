# Project Charter - Entendimiento del Negocio

## Nombre del Proyecto

Detección de neumonía con base en imagen de rayos X de región torácica

## Objetivo del Proyecto

Detectar condición de neumonía en pacientes potenciales a través del análisis de imágenes de resultados de rayos X de región torácica

## Alcance del Proyecto

### Incluye:

- Se cuenta con un conjunto de datos de alrededor de 5.800 imágenes de rayos X de la zona torácica de diferentes con y sin sintomatología de neumonía. Las imágenes cuentan además con una resolución considerable que permite la experimentación a un nivel de detalle sobresaliente.
- Se busca crear un modelo que, a partir de la imagen de rayos X de la zona torácica de un paciente, permita decidir si el paciente padece de neumonía.
- El modelo debe ser capaz de predecir con una precisión de al menos un 80% el estado del paciente en relación a afectación por neumonía. Así mismo, el desempeño del mismo no debe exceder más de 5 segundos para generar una predicción a partir de una imagen.

### Excluye:

- No se incluirá información proveniente de otras fuentes como datos básicos del paciente, muestras de sangre, o cualquier tipo de medición externa que no sea representada por la imagen de rayos X de la región torácica del paciente
- No se incluirán salidas distintas a la probabilidad de padecer neumonía para cada paciente, siendo el modelo implementado capaz de predecir un único valor de salida

## Metodología

Se seguirá una metodología basada en CRISP-DM. Se inicia por tanto con un proceso de entendimiento del negocio, realizando un trabajo de identificación del proyecto, objetivos, y propósito del mismo. Posteriormente, se realiza un proceso de revisión y entendimiento de los datos que se tienen para el caso; dado que se cuenta con datos de imágenes, se realizará una examinación de su formato, codificación, tamaño, entre otras características.

El siguiente paso consistirá de un proceso de preparación de los datos. Se espera que se realicen por tanto transformaciones de reescalado de imagenes, ajuste de formato RGB a escala de grises, eliminación de valores de pixeles fuera de rango, entre otros.

Se continuará con el diseño e implementación de un modelo que permita procesar la información de las imágenes listas y generar a partir de estas la predicción de estado del paciente en relación a afectación por neumonía. Así mismo, se procede con la evaluación de este modelo sobre un conjunto de métricas comunes para problemas de clasificación binaria, como la precisión y la pérdida calculada a partir de definiciones comunes como entropía cruzada binaria. La evaluación se realiza sobre datos no antes usados para el entrenamiento del modelo a fin de validar su capacidad de generalización con datos nuevos. A partir de esta evaluación se realiza una revisión sobre el entendimiento original y la silueta de estos resultados sobre el negocio.

Finalmente, se realiza un despliegue del modelo final validado, de tal manera que este sea capaz de recibir imágenes reales y nuevas de rayos X de pacientes y permitan predecir si el paciente padece o no de neumonía.

## Cronograma

| Etapa                                        | Duración Estimada | Fechas                         |
| -------------------------------------------- | ----------------- | ------------------------------ |
| Entendimiento del negocio y carga de datos   | 2 semanas         | del 23 de junio al 3 de julio  |
| Preprocesamiento, análisis exploratorio      | 1 semana          | del 4 de julio al 10 de junio  |
| Modelamiento y extracción de características | 3 semana          | del 4 de julio al 29 de julio  |
| Despliegue                                   | 2 semanas         | del 17 de julio al 29 de julio |
| Evaluación y entrega final                   | 3 semanas         | del 24 de julio al 29 de julio |

Hay que tener en cuenta que estas fechas son de ejemplo, estas deben ajustarse de acuerdo al proyecto.

## Equipo del Proyecto

- Miguel Angel Puentes Cespedes
- Cristian Danilo Romero Orjuela
- Edgar Daniel González Díaz

## Presupuesto

Se estructura un presupuesto como se muestra:

| Concepto                          | Valor unitario | Medida                                             | Unidades | Total           | Observaciones                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| :-------------------------------- | -------------- | -------------------------------------------------- | -------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Hora laborada                     | COP $ 40.000   | Hora por persona                                   | 48       | COP $ 1'920.000 | Estimada semana de trabajo con 4 horas laborales efectivas, por 4 semanas y con un equipo de 3 personas                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Recursos en nube (Cómputo)        | COP $ 2.062,5  | Hora de uso                                        | 48       | COP $ 99.000    | Estimado a partir de referencia de Databricks.com (Calculadora de precios): [https://www.databricks.com/product/pricing/product-pricing/instance-types]. Se estima el uso de la nube de AWS con un tipo de instancia de cómputo m4.xlarge (4 CPUS, 16GB RAM), con 3 instancias (una por persona) por la misma cantidad de horas laborales estimadas para el proyecto. El modelo de precios para esta instancia sería de tipo All-Purpose ($0.4125 por hora para el tipo de instancia mencionado). Se considera un valor de USD por peso colombiano de 5.000. Se realiza la estimaciòn para la regiòn Norte de Virginia (us-centra-1) |
| Recursos en nube (Almacenamiento) | COP $ 114      | GB de almacenamiento por mes                       | 50       | COP $ 5.750     | Se estima un total de 50 GB de almacenamiento de datos en formato .parquet dentro del lago de datos gestionado por Databricks. Los costos se estiman para un lago de datos almacenado en un bucket S3 de AWS.                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Servicio del modelo               | COP $ 350      | Hora de uso de Model Serving de Databricks por DBU | 640      | COP $ 224.000   | Se estima un llamado al modelo cada 10 segundos en entorno de despliegue por alrededor de un mes. Estimando una ejecución del modelo de 30 segundos por llamado. Se estima que la cantidad de horas de servicio en 8 horas por día, en 5 días habiles a la semana y 4 semanas en el mes sea de 160 horas. Así mismo, cada hora representa 4 DBUs o unidades de cómputo de databricks, generando así una cantidad de 640 horas x DBU. Se usa la calculadora de precios de databricks para estimar este costo.                                                                                                                         |

## Stakeholders

- Médicos especialistas
- Los médicos especializados serán los principales usuarios del modelo, siendo estos capaces de enviar una imagen de radiografía tomada a un paciente en formato digital, y recibir una predicción del estado del paciente en relación a su afectación por neumonía.
- Los médicos esperarán un buen desempeño del modelo, arrojando información útil para la toma de decisiones y el diagnóstico efectivo del paciente.

## Aprobaciones

- Validación y aprobación por parte de un médico especialista responsable, quien verificará que el modelo cumpla con los criterios clínicos y de precisión necesarios antes de su uso en entornos asistenciales.
