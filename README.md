# Team Data Science Project Template

Esta plantilla es una implementación de la plantilla de proyecto de Team Data Science Process que actualmente se utiliza en el "Programa de Formación en Machine Learning y Data Science" en la Universidad Nacional de Colombia.

Esta plantilla proporciona las siguientes carpetas y archivos:

- `src`: acá debe ir el código o implementación del proyecto en Python.
- `docs`: en esta carpeta se encuentran las plantillas de los documentos definidos en la metodología.
- `scripts`: esta carpeta debe contener los scripts/notebooks que se ejecutarán.
- `pyproject.toml`: archivo de definición del proyecto en Python.

## Instrucciones de Ejecución

Este proyecto está compuesto por múltiples servicios Docker organizados por fases del proceso de ciencia de datos: descarga, ETL, preprocesamiento y visualización.

> Asegúrate de tener instalado `Docker` y `docker-compose`.

### 1. Construir la imagen base

Cada servicio definido en el archivo `docker-compose.yml` representa una etapa específica. Puedes ejecutarlos individualmente así:

```bash
docker compose up --build nombre_servicio
```
