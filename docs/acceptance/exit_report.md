# Informe de Salida

## Resumen Ejecutivo

Este informe documenta los resultados del proyecto de Machine Learning **"Detección de neumonía con base en imagen de rayos X de región torácica"**, el cual siguió la metodología **CRISP-DM**. El objetivo principal fue desarrollar un modelo capaz de detectar la neumonía a partir de imágenes de rayos X de la región torácica con una **precisión mínima del 80%**.

Inicialmente se implementó un modelo final basado en **Redes Neuronales Convolucionales (CNN)** y se comparó con un modelo base de **Random Forest Classifier**. A pesar de utilizar técnicas avanzadas de aumentación de datos, regularización (Dropout, Batch Normalization) y entrenamiento (Early Stopping), el modelo CNN final alcanzó una **precisión del 88.59%** en el conjunto de prueba, superando significativamente la precisión del modelo base (73.72%). Sin embargo, la brecha entre la precisión de entrenamiento y validación nos indicó que, aunque se hicieron avances, el modelo aún enfrenta desafíos de generalización.

## Los principales logros fueron el desarrollo de un modelo robusto que supera al _baseline_ y la identificación de métricas clave como **Recall (0.92)** y **F1 Score (0.89)**, vitales en un contexto médico.

Además, se implementó un flujo de trabajo reproducible con versionamiento, lo que permitió mantener un control riguroso sobre los experimentos, configuraciones y resultados a lo largo del proyecto.

Las lecciones aprendidas resaltan la importancia de la calidad y cantidad de datos para problemas complejos de visión por computadora, especialmente la disponibilidad de más datos de validación, que en este caso resultó ser un factor crítico para mejorar la capacidad de generalización del modelo.

Las recomendaciones futuras se centran en el aprendizaje por transferencia y una mayor experimentación con la aumentación de datos y la arquitectura del modelo para seguir optimizando el desempeño y cumplir el objetivo inicial.
## Resultados del Proyecto

### Entregables y Logros Alcanzados por Etapa (CRISP-DM)

El proyecto se desarrolló siguiendo rigurosamente la metodología **CRISP-DM**, lo que permitió mantener un enfoque estructurado y trazable en todas las etapas, desde el entendimiento del problema hasta la evaluación y despliegue del modelo.

#### 1. Entendimiento del Negocio

- **Logro**: Se definió claramente el **objetivo del proyecto**: desarrollar un modelo de aprendizaje automático capaz de detectar neumonía en imágenes de rayos X torácicas pediátricas. Se establecieron métricas de éxito concretas, incluyendo una **precisión mínima del 80%** y un **tiempo de predicción máximo de 5 segundos** por imagen.
- **Adicionalmente**, se identificó y describió que el conjunto de datos utilizado proviene del **Guangzhou Women and Children’s Medical Center** y está disponible públicamente en [Kaggle](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia). Este contiene radiografías pediátricas (niños de 1 a 5 años) etiquetadas por médicos especialistas y organizadas para su uso en proyectos de clasificación médica.

- **Entregable**: Se generó un **Project Charter** documentando el nombre del proyecto, objetivo, alcance (5.800 imágenes), métricas de éxito, limitaciones (solo una condición médica, sin segmentación anatómica), y restricciones tecnológicas. Este documento sirvió como guía para la planificación, comunicación y evaluación de resultados del proyecto.

#### 2. Entendimiento de los Datos

- **Logro**: Se realizó un análisis exploratorio y técnico del dataset original, permitiendo:

  - Comprender la **estructura jerárquica del dataset**, dividido en carpetas `train`, `val` y `test`, y cada una con subdirectorios `NORMAL` y `PNEUMONIA`.
  - Identificar un **importante desbalance de clases** en los datos de entrenamiento, con mayor proporción de imágenes con diagnóstico de neumonía.
  - Detectar una **limitación crítica en la cantidad de datos de validación**, lo que representa un riesgo de sobreajuste y dificulta una evaluación robusta del modelo.
  - Evaluar la **calidad y consistencia de las imágenes**, descartando aquellas corruptas o vacías mediante un script automatizado.

- **Entregable**:
  - Un **diccionario de datos** detallado que describe las variables y estructuras de las bases `bronze`, `silver` y `gold`.
  - Un **reporte exploratorio (EDA)** que incluye visualizaciones de la distribución de clases, análisis PCA y estadísticas de pixelado.
  - Documentación del flujo de almacenamiento en entorno tipo **Lakehouse**, con separación por capas (`bronze`, `silver`, `gold`) y uso del formato `.parquet` para análisis eficiente.

#### 3. Preparación de los Datos

- **Logro**: Se diseñó e implementó un pipeline **ETL reproducible y versionado usando Docker**, que automatiza la preparación de datos desde su forma cruda hasta un formato óptimo para modelado. Las acciones clave incluyeron:

  - **Carga automática de datos** desde la API de Kaggle, organizando las imágenes en la carpeta `bronze`.
  - Transformación de imágenes en pandas:
    - Conversión a escala de grises y redimensionamiento a **128x128 píxeles**.
    - Verificación de integridad, codificación de etiquetas y almacenamiento en formato `.parquet` (`silver`).
  - Generación de la base `gold`, en la que cada imagen fue convertida a un vector numérico de **16,384 píxeles** para modelos tabulares.
  - Implementación de **técnicas de aumentación de datos** para el conjunto de entrenamiento, incluyendo rotaciones, traslaciones, inversión horizontal y zoom aleatorio, con el fin de mejorar la generalización del modelo.

- **Entregable**:
  - **Scripts de procesamiento** organizados en `scripts/data_acquisition` y `scripts/preprocessing`, con control de versiones para asegurar reproducibilidad.
  - **Bases de datos estructuradas** en las rutas `src/Pneumonia_Detection/database/{bronze|silver|gold}` según el nivel de transformación.
  - Separación clara de los datos en particiones `train`, `val` y `test`, asegurando consistencia entre etapas.
  - Conjunto de datos listo para diferentes enfoques de modelado: imágenes en formato binario para CNNs (silver) y vectores planos para modelos tradicionales como Random Forest (gold).

#### 4. Modelado

- **Logro**:
  - **Modelo Base (Random Forest Classifier)** con 16,384 características.
  - **Modelo Final (CNN)** en Keras con capas `Conv2D`, `BatchNormalization`, `MaxPooling2D` y `Dropout`, y _callbacks_ como `EarlyStopping`.
- **Entregable**: Modelos entrenados y código fuente asociado.

#### 5. Evaluación

- **Logro**: Evaluación de métricas clave, comparación entre modelos, análisis de sobreajuste.
- **Entregable**: "Reporte del Modelo Final" y "Reporte del Modelo Baseline" con precisión, curvas de entrenamiento y matriz de confusión.

#### 6. Despliegue

- **Logro**: Se diseñó e implementó un flujo de despliegue funcional para exponer el modelo entrenado como un servicio web capaz de recibir nuevas imágenes y generar predicciones en tiempo real.
- **Entregable**: Documento conceptual y técnico del despliegue, incluyendo definición de infraestructura, requisitos del entorno, endpoints REST, instrucciones de instalación y uso, así como consideraciones de seguridad y mantenimiento.

---

### Evaluación del Modelo Final y Comparación con el Modelo Base

- **Precisión del Modelo Final (CNN)**: **88.59%**
- **Precisión del Modelo Base (Random Forest)**: **73.72%**

#### Matriz de Confusión (CNN):

- 60 **falsos positivos**
- 29 **falsos negativos**

#### Métricas relevantes:

- **Recall**: 0.92
- **Precisión**: 0.85
- **F1 Score**: 0.89

---

### Descripción de los Resultados y su Relevancia para el Negocio

Los resultados demuestran la viabilidad de ML para detección de neumonía desde rayos X.

#### Relevancia para el negocio:

- **Apoyo al Diagnóstico Clínico**
- **Eficiencia Operacional**
- **Estandarización**

La alta sensibilidad (0.92) es crítica para minimizar falsos negativos.

---

## Lecciones Aprendidas

### Principales Desafíos y Obstáculos

- Escasez de imágenes de validación → sobreajuste.
- Complejidad del problema de detección.
- Dificultad de balancear precisión y generalización.

### Lecciones sobre Manejo de Datos, Modelado e Implementación

#### Manejo de Datos:

- Aumentación es clave con datasets limitados.
- Reescalado y normalización son esenciales.

#### Modelado:

- CNNs son superiores a modelos clásicos en visión por computadora.
- Regularización y _callbacks_ ayudan contra sobreajuste.

#### Implementación:

- Arquitectura secuencial de Keras facilita prototipado.
- Ajuste de hiperparámetros es crítico.

### Recomendaciones Futuras

1. **Transfer Learning:** Usar modelos preentrenados (e.g., ResNet, VGG, EfficientNet) para mejorar el rendimiento con menos datos.
2. **Aumentación Avanzada:** Aplicar técnicas como GANs o AutoAugment para generar datos sintéticos y enriquecer el entrenamiento.
3. **Más Datos:** Recolectar más imágenes balanceadas para mejorar la generalización del modelo.
4. **Tuning con Keras Tuner:** Optimizar hiperparámetros automáticamente mediante búsqueda eficiente .
5. **Probar Distintas Arquitecturas:** Evaluar múltiples CNN (MobileNet, DenseNet, etc.) para encontrar la más adecuada.
6. **Análisis de Errores:** Estudiar falsos positivos/negativos para guiar mejoras en el modelo y los datos.

---

## Impacto del Proyecto

### Impacto del Modelo en el Negocio o Industria

- **Acelera el diagnóstico**.
- **Estandariza la evaluación clínica**.
- **Permite detección temprana**.
- **Impulsa la salud digital**.

---

### Áreas de Mejora y Futuras Oportunidades

- **Aumentar precisión y generalización**.
- **Integración con sistemas clínicos**.
- **Validación clínica y certificación**.
- **Expansión a otras patologías**.
- **Incorporar explicabilidad e incertidumbre**.

---

## Conclusiones

### Resumen de Resultados y Logros

El modelo CNN alcanzó una precisión del **88.59%**, superando al modelo base y mostrando métricas sólidas:

- **Recall**: 0.92
- **F1 Score**: 0.89

Se aplicó con éxito la metodología CRISP-DM, se implementaron técnicas de aumentación y regularización, y se logró un modelo prometedor.

---

### Conclusiones Finales y Recomendaciones

Aunque no se alcanzó el umbral de precisión inicial (80%) según el _Project Charter_, se logró superarlo ampliamente.

Para futuros proyectos:

- **Aplicar Transfer Learning**
- **Mejorar aumentación de datos**
- **Recolectar más datos**
- **Optimizar hiperparámetros**
- **Asegurar explicabilidad y evaluación clínica**

Estas acciones permitirán escalar hacia un modelo clínicamente aplicable y confiable.

---
