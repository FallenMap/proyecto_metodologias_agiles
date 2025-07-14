import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from typing import Dict, Any

# Agregar al path el directorio src para importar los módulos personalizados
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from Pneumonia_Detection.models.cnn_model import PneumoniaCNN
from Pneumonia_Detection.models.baseline_model import PneumoniaRandomForest

# Cargar resultados de los modelos desde los directorios especificados
def cargar_resultados_modelos(output_dir: str) -> Dict[str, Any]:
    model_dir = Path(output_dir) / Path("models")
    results_dir = Path(output_dir) / Path("results")

    model_cnn = PneumoniaCNN('v1')
    model_cnn.load_model(model_dir)
    model_cnn.load_results(results_dir)
    outputs_cnn = model_cnn.output_results

    model_linebase = PneumoniaRandomForest('v2')
    model_linebase.load_model(model_dir)
    model_linebase.load_results(results_dir)
    outputs_linebase = model_linebase.output_results

    return {
        "cnn": outputs_cnn,
        "baseline": outputs_linebase
    }

# Crear gráficos de comparación entre modelos
def crear_graficos_comparacion(resultados: Dict[str, Any], output_dir: str):
    output_dir = Path(output_dir) / Path("plots")
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))

    modelos = []
    precisiones = []

    if 'cnn' in resultados:
        modelos.append('TensorFlow CNN')
        precisiones.append(resultados['cnn']['test_accuracy'])

    if 'baseline' in resultados:
        modelos.append('Random Forest')
        precisiones.append(resultados['baseline']['test_accuracy'])

    plt.bar(modelos, precisiones, color=['#FF6B6B', '#4ECDC4'])
    plt.title('Comparación de precisiones de modelos')
    plt.ylabel('Precisión')
    plt.ylim(0, 1)

    for i, v in enumerate(precisiones):
        plt.text(i, v + 0.01, f'{v:.4f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(output_dir / 'comparacion_precision.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Curvas de entrenamiento para CNN
    if 'cnn' in resultados and 'training_history' in resultados['cnn']:
        historia = resultados['cnn']['training_history']

        plt.figure(figsize=(12, 4))

        plt.subplot(1, 2, 1)
        plt.plot(historia['loss'], label='Pérdida entrenamiento')
        plt.plot(historia['val_loss'], label='Pérdida validación')
        plt.title('Modelo CNN - Pérdida')
        plt.xlabel('Época')
        plt.ylabel('Pérdida')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(historia['accuracy'], label='Precisión entrenamiento')
        plt.plot(historia['val_accuracy'], label='Precisión validación')
        plt.title('Modelo CNN - Precisión')
        plt.xlabel('Época')
        plt.ylabel('Precisión')
        plt.legend()

        plt.tight_layout()
        plt.savefig(output_dir / 'curvas_entrenamiento_tensorflow.png', dpi=300, bbox_inches='tight')
        plt.close()

    # Importancia de características del modelo baseline
    if 'baseline' in resultados and 'feature_importance_top_10' in resultados['baseline']:
        importancia_datos = resultados['baseline']['feature_importance_top_10']

        if importancia_datos:
            caracteristicas = [item['feature'] for item in importancia_datos]
            importancia = [item['importance'] for item in importancia_datos]

            plt.figure(figsize=(10, 6))
            plt.barh(caracteristicas, importancia, color='#4ECDC4')
            plt.title('Random Forest - Top 10 Características')
            plt.xlabel('Importancia')
            plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.savefig(output_dir / 'importancia_caracteristicas_baseline.png', dpi=300, bbox_inches='tight')
            plt.close()

# Generar informe de comparación entre modelos
def generar_informe_comparacion(resultados: Dict[str, Any], output_dir: str):
    output_dir = Path(output_dir) / Path("plots")
    output_dir.mkdir(parents=True, exist_ok=True)

    informe = {
        'resumen': {},
        'comparacion_detallada': {},
        'recomendaciones': []
    }

    # Estadísticas resumen
    if 'cnn' in resultados and 'baseline' in resultados:
        tf_acc = resultados['cnn']['test_accuracy']
        baseline_acc = resultados['baseline']['test_accuracy']

        informe['resumen'] = {
            'precision_tensorflow': tf_acc,
            'precision_baseline': baseline_acc,
            'diferencia_precision': tf_acc - baseline_acc,
            'mejor_modelo': 'TensorFlow CNN' if tf_acc > baseline_acc else 'Random Forest'
        }

        # Recomendaciones
        if tf_acc > baseline_acc:
            informe['recomendaciones'].append(
                "TensorFlow CNN se desempeña mejor que Random Forest baseline"
            )
        else:
            informe['recomendaciones'].append(
                "Random Forest baseline se desempeña mejor que TensorFlow CNN"
            )

        if abs(tf_acc - baseline_acc) < 0.05:
            informe['recomendaciones'].append(
                "Los modelos se desempeñan de forma similar"
            )

    if 'cnn' in resultados:
        informe['comparacion_detallada']['cnn'] = {
            'precision_prueba': resultados['cnn']['test_accuracy'],
            'perdida_prueba': resultados['cnn'].get('test_loss', 'N/A'),
            'tipo_modelo': 'Red Neuronal Convolucional',
            'ventajas': [
                'Puede capturar patrones espaciales en imágenes',
                'Aprende características jerárquicas',
                'Adecuado para clasificación compleja de imágenes'
            ],
            'desventajas': [
                'Requiere más recursos computacionales',
                'Tiempo de entrenamiento más largo',
                'Más hiperparámetros para ajustar'
            ]
        }

    if 'baseline' in resultados:
        informe['comparacion_detallada']['baseline'] = {
            'precision_prueba': resultados['baseline']['test_accuracy'],
            'tipo_modelo': 'Random Forest',
            'ventajas': [
                'Entrenamiento y predicción rápidos',
                'Proporciona importancia de características',
                'Menor riesgo de sobreajuste',
                'Fácil de interpretar'
            ],
            'desventajas': [
                'No capta relaciones espaciales',
                'Limitado a datos tabulares',
                'Puede no capturar patrones complejos'
            ]
        }

    # Guardar informe JSON
    ruta_json = output_dir / 'informe_comparacion_modelos.json'
    with open(ruta_json, 'w') as f:
        json.dump(informe, f, indent=2)

    # Crear informe en formato markdown
    markdown = generar_informe_markdown(informe)
    ruta_md = output_dir / 'informe_comparacion_modelos.md'
    with open(ruta_md, 'w') as f:
        f.write(markdown)

    return informe

# Generar informe en Markdown
def generar_informe_markdown(informe: Dict[str, Any]) -> str:
    md = "# Informe de Comparación de Modelos\n\n"

    if informe['resumen']:
        resumen = informe['resumen']
        md += "## Resumen\n\n"
        md += f"- **Precisión TensorFlow CNN**: {resumen.get('precision_tensorflow', 'N/A'):.4f}\n"
        md += f"- **Precisión Random Forest**: {resumen.get('precision_baseline', 'N/A'):.4f}\n"
        md += f"- **Diferencia de Precisión**: {resumen.get('diferencia_precision', 'N/A'):.4f}\n"
        md += f"- **Mejor Modelo**: {resumen.get('mejor_modelo', 'N/A')}\n\n"

    md += "## Comparación Detallada\n\n"

    if 'cnn' in informe['comparacion_detallada']:
        cnn = informe['comparacion_detallada']['cnn']
        md += "### TensorFlow CNN\n\n"
        md += f"- **Precisión**: {cnn['precision_prueba']:.4f}\n"
        md += f"- **Tipo de Modelo**: {cnn['tipo_modelo']}\n"
        md += f"- **Pérdida de Prueba**: {cnn.get('perdida_prueba', 'N/A')}\n\n"

        md += "**Ventajas**:\n"
        for v in cnn['ventajas']:
            md += f"- {v}\n"
        md += "\n**Desventajas**:\n"
        for d in cnn['desventajas']:
            md += f"- {d}\n"
        md += "\n"

    if 'baseline' in informe['comparacion_detallada']:
        bl = informe['comparacion_detallada']['baseline']
        md += "### Random Forest Baseline\n\n"
        md += f"- **Precisión**: {bl['precision_prueba']:.4f}\n"
        md += f"- **Tipo de Modelo**: {bl['tipo_modelo']}\n\n"

        md += "**Ventajas**:\n"
        for v in bl['ventajas']:
            md += f"- {v}\n"
        md += "\n**Desventajas**:\n"
        for d in bl['desventajas']:
            md += f"- {d}\n"
        md += "\n"

    if informe['recomendaciones']:
        md += "## Recomendaciones\n\n"
        for r in informe['recomendaciones']:
            md += f"- {r}\n"

    return md

# Función principal
def main():
    # Configuración
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "../artifacts/comparison")

    print("Iniciando comparación de modelos...")
    print(f"Directorio de salida: {OUTPUT_DIR}")

    # Cargar resultados
    resultados = cargar_resultados_modelos(OUTPUT_DIR)

    if not resultados:
        print("¡No se encontraron resultados de modelos!")
        return

    # Crear gráficos de comparación
    print("Creando gráficos de comparación...")
    crear_graficos_comparacion(resultados, OUTPUT_DIR)

    # Generar informe de comparación
    print("Generando informe de comparación...")
    informe = generar_informe_comparacion(resultados, OUTPUT_DIR)

    print("¡Comparación de modelos completada!")
    print(f"Resultados guardados en: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
