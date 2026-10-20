import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def crear_directorios():
    os.makedirs('resultados/tablas', exist_ok=True)
    os.makedirs('resultados/figuras', exist_ok=True)

def main():
    crear_directorios()
    ruta_archivo = 'datos/seismic_data.csv' 
    
    print("Iniciando análisis exploratorio...")
    
    try:
        df = pd.read_csv(ruta_archivo, sep=None, engine='python')
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return
        
    # 1. LIMPIEZA DE COLUMNAS 
    df.columns = df.columns.str.strip().str.lower()
    df = df.loc[:, ~df.columns.duplicated()] 
    columnas = df.columns.tolist()
    
    # 2. BUSCADOR INTELIGENTE DE VARIABLES
    posibles_mag = [c for c in columnas if c in ['mag', 'magnitude', 'magnitud', 'm', 'ml']]
    if posibles_mag:
        col_mag = posibles_mag[0]
    else:
        num_cols = [c for c in df.select_dtypes(include='number').columns if 'lat' not in c and 'lon' not in c and 'depth' not in c]
        col_mag = num_cols[0] if num_cols else df.select_dtypes(include='number').columns[0]
        
    posibles_depth = [c for c in columnas if c in ['depth', 'profundidad', 'z']]
    if posibles_depth:
        col_depth = posibles_depth[0]
    else:
        num_cols = [c for c in df.select_dtypes(include='number').columns if c != col_mag and 'lat' not in c and 'lon' not in c]
        col_depth = num_cols[0] if num_cols else df.select_dtypes(include='number').columns[-1]

    posibles_time = [c for c in columnas if 'time' in c or 'date' in c or 'fecha' in c]
    col_time = posibles_time[0] if posibles_time else columnas[0]
    
    cols_cat = [c for c in df.select_dtypes(include=['object', 'string']).columns if c not in [col_time, 'id', 'updated', 'net']]
    preferidas = [c for c in cols_cat if c in ['type', 'tipo', 'place', 'region', 'magtype']]
    col_type = preferidas[0] if preferidas else (cols_cat[0] if cols_cat else df.columns[-1])
    
    print(f"-> Variables detectadas | Magnitud: '{col_mag}' | Profundidad: '{col_depth}' | Tiempo: '{col_time}' | Categoría: '{col_type}'")
    
    print(f"Registros iniciales cargados: {len(df)}")
    
    print("\n[1] Diagnóstico de Calidad")
    nulos_antes = df.isnull().sum()
    duplicados_antes = df.duplicated().sum()
    pd.DataFrame({'Valores Nulos': nulos_antes}).to_csv('resultados/tablas/diagnostico_nulos.csv')
    print(f"Duplicados encontrados: {duplicados_antes}")
    
    print("\n[2] Limpieza y Preparación")
    df_limpio = df.drop_duplicates().copy()
    df_limpio = df_limpio.dropna(subset=[col_mag, col_depth, col_time])
    
    # --- CORRECCIÓN DEL FORMATO DE FECHA UNIX ---
    serie_tiempo = df_limpio[col_time]
    if isinstance(serie_tiempo, pd.DataFrame):
        serie_tiempo = serie_tiempo.iloc[:, 0]
        
    if pd.api.types.is_numeric_dtype(serie_tiempo):
        serie_convertida = pd.to_datetime(serie_tiempo, unit='ms', errors='coerce', utc=True)
    else:
        serie_convertida = pd.to_datetime(serie_tiempo, errors='coerce', utc=True)
    
    df_limpio = df_limpio.drop(columns=[col_time])
    df_limpio[col_time] = serie_convertida
    df_limpio = df_limpio.dropna(subset=[col_time])
    
    print(f"Registros finales válidos: {len(df_limpio)}")
    
    print("\n[3] Generando Estadísticas Descriptivas")
    # Estadísticas numéricas generales
    stats_num = df_limpio[[col_mag, col_depth]].describe()
    stats_num.to_csv('resultados/tablas/estadisticas_numericas.csv')
    
    # Frecuencia de categorías
    freq_tipo = df_limpio[col_type].value_counts().reset_index()
    freq_tipo.columns = ['Categoría', 'Frecuencia']
    freq_tipo.to_csv('resultados/tablas/frecuencia_categorias.csv', index=False)

    # --- NUEVA SECCIÓN AGREGADA: AGREGACIÓN POR GRUPOS ---
    # Calcula el promedio de magnitud y profundidad por cada categoría
    stats_grupos = df_limpio.groupby(col_type)[[col_mag, col_depth]].mean().reset_index()
    stats_grupos.to_csv('resultados/tablas/estadisticas_por_grupo.csv', index=False)
    # --------------------------------------------------------
    
    print("\n[4] Generando Visualizaciones")
    sns.set_theme(style="whitegrid")
    
    # 1. Distribución
    plt.figure(figsize=(8, 5))
    sns.histplot(df_limpio[col_mag], bins=40, kde=True, color='steelblue')
    plt.title('Distribución de la Magnitud')
    plt.xlabel(col_mag.capitalize())
    plt.ylabel('Frecuencia')
    plt.tight_layout()
    plt.savefig('resultados/figuras/1_distribucion.png')
    plt.close()

    # 2. Valores extremos
    plt.figure(figsize=(8, 5))
    sns.boxplot(x=df_limpio[col_depth], color='lightgreen')
    plt.title('Dispersión y Valores Extremos de Profundidad')
    plt.xlabel(col_depth.capitalize())
    plt.tight_layout()
    plt.savefig('resultados/figuras/2_extremos.png')
    plt.close()

    # 3. Relación
    tipos_principales = df_limpio[col_type].value_counts().head(3).index
    df_top_tipos = df_limpio[df_limpio[col_type].isin(tipos_principales)]
    
    if len(df_top_tipos) > 10000:
        df_muestra = df_top_tipos.sample(n=10000, random_state=42)
    else:
        df_muestra = df_top_tipos

    plt.figure(figsize=(9, 6))
    sns.scatterplot(data=df_muestra, x=col_mag, y=col_depth, hue=col_type, alpha=0.5)
    plt.title('Relación Magnitud vs Profundidad por Categoría (Muestra 10k)')
    plt.xlabel(col_mag.capitalize())
    plt.ylabel(col_depth.capitalize())
    plt.gca().invert_yaxis() 
    plt.tight_layout()
    plt.savefig('resultados/figuras/3_relacion_grupos.png')
    plt.close()

    # 4. Barras
    plt.figure(figsize=(9, 5))
    sns.barplot(data=freq_tipo.head(5), x='Frecuencia', y='Categoría', hue='Categoría', palette='viridis', legend=False)
    plt.title('Top 5 Categorías Principales')
    plt.xlabel('Cantidad de Registros')
    plt.ylabel(col_type.capitalize())
    plt.tight_layout()
    plt.savefig('resultados/figuras/4_comparacion_categorias.png')
    plt.close()

    # 5. Evolución temporal
    plt.figure(figsize=(10, 5))
    df_temporal = df_limpio.set_index(col_time).resample('YE').size()
    df_temporal.plot(color='crimson')
    plt.title('Evolución Temporal de Sismos Anuales')
    plt.xlabel('Fecha (Año)')
    plt.ylabel('Total de Eventos')
    plt.tight_layout()
    plt.savefig('resultados/figuras/5_evolucion_temporal.png')
    plt.close()
    
    print("\n[5] Exportando dataset final")
    if len(df_limpio) > 100000:
        df_limpio.sample(n=50000, random_state=42).to_csv('resultados/datos_procesados_muestra.csv', index=False)
        print("Nota: Se guardó una muestra de 50.000 registros para facilitar el envío a Canvas.")
    else:
        df_limpio.to_csv('resultados/datos_procesados.csv', index=False)
        
    print("Script finalizado exitosamente. Las imágenes y tablas ya están en la carpeta 'resultados'.")

if __name__ == '__main__':
    main()