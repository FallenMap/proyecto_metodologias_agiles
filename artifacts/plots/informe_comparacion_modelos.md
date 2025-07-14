# Informe de Comparación de Modelos

## Resumen

- **Precisión TensorFlow CNN**: 0.6250
- **Precisión Random Forest**: 0.5625
- **Diferencia de Precisión**: 0.0625
- **Mejor Modelo**: TensorFlow CNN

## Comparación Detallada

### TensorFlow CNN

- **Precisión**: 0.6250
- **Tipo de Modelo**: Red Neuronal Convolucional
- **Pérdida de Prueba**: 29.12999153137207

**Ventajas**:
- Puede capturar patrones espaciales en imágenes
- Aprende características jerárquicas
- Adecuado para clasificación compleja de imágenes

**Desventajas**:
- Requiere más recursos computacionales
- Tiempo de entrenamiento más largo
- Más hiperparámetros para ajustar

### Random Forest Baseline

- **Precisión**: 0.5625
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
