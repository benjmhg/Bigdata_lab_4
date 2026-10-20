# Laboratorio: Análisis Exploratorio de Datos (EDA) - Eventos Sísmicos

Este proyecto contiene un proceso automatizado y reproducible en Python para realizar un Análisis Exploratorio de Datos (EDA) sobre un registro global de eventos sísmicos. El script diagnostica la calidad de los datos, genera estadísticas descriptivas y exporta visualizaciones relevantes.

## 1. Requisitos Previos
- **Python:** Versión 3.8 o superior.
- Gestor de paquetes `pip` instalado.

## 2. Instalación de Dependencias
Abre una terminal en la carpeta principal del proyecto y ejecuta el siguiente comando para instalar las bibliotecas necesarias:

```bash
pip install -r requirements.txt
```

## 3. Ubicación y Descarga del Dataset
Debido a que el dataset original contiene más de 3.4 millones de registros y supera los 100 MB, no se adjuntó en el archivo ZIP para cumplir con las restricciones de tamaño de Canvas.

Para reproducir el análisis, debes descargar el archivo original siguiendo estas instrucciones:
1. Crear una carpeta llamada `datos` en la raíz del proyecto.
2. Descargar el dataset original ("The Ultimate Earthquake Dataset from 1990-2023") desde Kaggle haciendo clic en el siguiente enlace:
   [https://www.kaggle.com/datasets/alessandrolobello/the-ultimate-earthquake-dataset-from-1990-2023?resource=download](https://www.kaggle.com/datasets/alessandrolobello/the-ultimate-earthquake-dataset-from-1990-2023?resource=download)
3. Extraer el archivo `.csv` descargado y guardarlo con el nombre `seismic_data.csv` dentro de la carpeta `datos/`.

## 4. Ejecución del Análisis
Para ejecutar el proceso completo sin intervención manual, sitúate en la raíz del proyecto y ejecuta el script principal en la terminal:

```bash
python analisis_exploratorio.py
```
*(Nota: Dependiendo de la configuración de tu sistema, el comando puede ser `python3` o `py` en lugar de `python`).*

## 5. Estructura de Resultados
Al finalizar la ejecución, el script generará automáticamente las siguientes carpetas y archivos si no existen:
- `resultados/tablas/`: Contiene los CSV con diagnósticos de calidad, frecuencias de categorías y estadísticas por grupos.
- `resultados/figuras/`: Contiene 5 gráficos en formato PNG con la distribución, valores extremos y relaciones de las variables (usando muestreo aleatorio reproducible para la dispersión).
- `resultados/datos_procesados_muestra.csv`: Dado el tamaño masivo del dataset original, el script exporta automáticamente una muestra aleatoria representativa de 50.000 registros ya limpios, cumpliendo con el mínimo exigido por la rúbrica y permitiendo su carga en la plataforma.