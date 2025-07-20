# Despliegue de modelos

## Infraestructura

- **Nombre del modelo:** Pneumonia detection
- **Plataforma de despliegue:** Se desplegó el proyecto en la plataforma Render mediante la definición de una imagen de docker encontrable en la raíz del proyecto con el nombre de archivo **Dockerfile**. En este archivo se expone el puerto correspondiente al servicio desarrollado, siendo este el número de puerto 8000.
  A través de Render, se construya la imagen del proyecto y se ejecuta en una máquina virtual aislada y gestionada por la plataforma de manera gratuita; cabe mencionar que existen ciertas consideraciones menores, como la inactividad del servicio en desuso hasta la recepción de una primera petición en un periodo de tiempo dado.
- **Requisitos técnicos:**
  Como se describe en la definición de imagen de Docker del archivo Dockerfile, se utiliza una versión de python 3.11, en conjunto con las librerías ampliamente descritas en el archivo requirements.txt, pero con las versiones enunciadas a continuación:

  - matplotlib==3.10.3
  - numpy==2.1.3
  - pandas==2.3.0
  - pillow==11.3.0
  - pyarrow==20.0.0
  - scikit-image==0.25.2
  - scikit-learn==1.7.0
  - seaborn==0.13.2
  - tensorflow==2.19.0

  El despliegue realizado funciona sobre una infraestructura relativamente ligera con 256 MB de memoria volátil (RAM) y 0.1 unidades de CPU virtual
  Se recomienda un sistema operativo Linux o Windows compatible con la versión de python: 3.11

- **Requisitos de seguridad:**
  No se tienen políticas estrictas con respecto a seguridad debido a las características públicas y de código abierto del proyecto. No se posee un método de autenticación definido para el llamado al endpoint HTTP expuesto por el servicio. Sin embargo, por defecto la plataforma se encarga de la encriptación de datos a través del protocolo HTTPs estándar, el cual permite la encriptación de información mediante un modelo asimétrico basado en la generación y uso de certificados.
  Se tiene una sección de validación de esquema que permite verificar las características de la imagen enviada a fin de permitir su correcta adaptación a la entrada esperada por el modelo.

- **Diagrama de arquitectura:**
  Se presentan los componentes que hacen parte del diagrama general de la arquitectura definida. Se definen además elementos de despliegue continuo a través de repositorio.
  Se utiliza un proveedor externo de despliegues documentado en: https://github.com/marketplace/actions/deploy-to-render. Así mismo, se crea un API Key para la autenticación de las peticiones realizadas para el re-despliegue del proyecto.

  ![Diagrama Arquitectura](./diagrams/diagram_infrastructure.jpg)

## Código de despliegue

- **Archivo principal:** El archivo principal de despliegue se localiza en la ruta **scripts/deploy/deploy.py**. Así mismo, se crea una imagen de docker en la raíz del proyecto con el nombre **Dockerfile**. De manera similar, se crea un nuevo servicio en el archivo definición de **docker-compose.yml** para generar el despliegue del servicio.
- **Rutas de acceso a los archivos:** Los archivos necesarios para el despliegue se encuentran en:
  - ./src: Archivos de código generales para la implementación de todo el esquema del servicio y la estructura de código dada
  - ./artifacts: Archivos de resultados de despliegues, incluyendo modelos guardados, imágenes de resultados y archivos resumen en formato JSON
  - ./scripts: Puntos de entrada a procesos varios, incluyendo visualización, entrenamiento de modelos, entre otros.
- **Variables de entorno:**
  Para el despliegue, se requiere de la ruta de acceso al archivo definición de los pesos el modelo. El identificador de esta variable de entorno es: **MODEL_PATH** (En general, esta ruta debería hacer referencia a un archivo en formato .h5 en la carpeta /artifacts)
  Se requiere además de la definición de la ruta raíz de Python: **PYTHONPATH** (por defecto /app/src)

## Documentación del despliegue

- **Instrucciones de instalación:** (instrucciones detalladas para instalar el modelo en la plataforma de despliegue)
- **Instrucciones de configuración:** (instrucciones detalladas para configurar el modelo en la plataforma de despliegue)
- **Instrucciones de uso:** (instrucciones detalladas para utilizar el modelo en la plataforma de despliegue)
- **Instrucciones de mantenimiento:** (instrucciones detalladas para mantener el modelo en la plataforma de despliegue)
