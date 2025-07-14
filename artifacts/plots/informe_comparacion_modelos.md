# Informe de Comparación de Modelos

## Resumen

- **Precisión TensorFlow CNN**: 0.7513
- **Precisión Random Forest**: 0.7372
- **Diferencia de Precisión**: 0.0141
- **Mejor Modelo**: TensorFlow CNN

## Comparación Detallada

### TensorFlow CNN

- **Precisión**: 0.7513
- **Tipo de Modelo**: Red Neuronal Convolucional
- **Pérdida de Prueba**: 1.243857741355896

**Ventajas**:
- Puede capturar patrones espaciales en imágenes
- Aprende características jerárquicas
- Adecuado para clasificación compleja de imágenes

**Desventajas**:
- Requiere más recursos computacionales
- Tiempo de entrenamiento más largo
- Más hiperparámetros para ajustar

### Random Forest Baseline

- **Precisión**: 0.7372
- **Tipo de Modelo**: Random Forest

**Ventajas**:
- Entrenamiento y predicción rápidos
- Proporciona importancia de características
- Menor riesgo de sobreajuste
- Fácil de interpretar

**Desventajas**:
- No capta relaciones espaciales
- Limitado a datos tabulares
- Puede no capturar patrones complejos

## Recomendaciones

- TensorFlow CNN se desempeña mejor que Random Forest baseline
- Los modelos se desempeñan de forma similar
