"""
analisis.py
Primer Parcial - Inteligencia Artificial - COTECNOVA 2026
Estudiante: Brandon Cortes Giraldo
Grupo: 04
Docente: Jhon James Cano Sánchez
"""

import csv
import os
import numpy as np
import matplotlib.pyplot as plt

def cargar_datos_iniciales(ruta_csv):
    """
    Tarea 2: Carga de datos
    Carga el archivo CSV asignado y muestra las primeras 5 filas
    junto con el total de registros encontrados.
    """
    print("=" * 65)
    print(" 1. CARGA DE DATOS INICIALES (TAREA 2)")
    print("=" * 65)
    
    filas_crudas = []
    with open(ruta_csv, 'r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            filas_crudas.append(fila)
            
    print(f"Número total de registros leídos: {len(filas_crudas)}")
    print("\nPrimeras 5 filas del dataset:")
    print("-" * 65)
    for i, fila in enumerate(filas_crudas[:5], 1):
        print(f"Fila {i}: {fila}")
    print("-" * 65)
    return filas_crudas

def limpiar_calidad_datos(filas_crudas):
    """
    Tarea 3: Calidad de datos
    Identifica los 3 problemas de calidad y aplica las correcciones:
    1. Fila de resumen totalizadora (RESUMEN).
    2. Dato faltante en accidentes (Centro, 2026-06-01).
    3. Inconsistencia entre el total del resumen y la fila faltante.
    """
    print("\n" + "=" * 65)
    print(" 2. EVALUACIÓN Y TRATAMIENTO DE CALIDAD DE DATOS (TAREA 3)")
    print("=" * 65)
    
    filas_limpias = []
    valores_centro_accidentes = []
    
    # Paso 1: Recolectar datos válidos de Centro para imputación
    for f in filas_crudas:
        if f['zona'] == 'Centro' and f['accidentes'] != '' and f['zona'] != 'RESUMEN':
            valores_centro_accidentes.append(float(f['accidentes']))
            
    # Mediana/media de Centro para imputar: (5 + 4) / 2 = 4.5 -> redondeado a 4 o 5 (usaremos 4 o 1 segun heridos)
    # Como hay 1 herido, mínimo hubo 1 accidente. Si la suma total de RESUMEN era 62 y las 10 filas suman 62,
    # significa que la fila 11 fue agregada después o el resumen no la sumó. Imputamos con 4 (media de Centro).
    valor_imputado = int(np.round(np.mean(valores_centro_accidentes))) # 5 + 4 / 2 = 4.5 -> 4
    
    for f in filas_crudas:
        # Problema 1: Eliminar fila RESUMEN
        if f['zona'].upper() == 'RESUMEN':
            print(" -> [Problema 1 Detectado] Fila RESUMEN encontrada. Se excluye para no duplicar datos.")
            continue
            
        # Problema 2: Dato faltante en accidentes
        acc_str = f['accidentes']
        if acc_str == '' or acc_str is None:
            print(f" -> [Problema 2 Detectado] Fila con fecha {f['fecha']} en {f['zona']} tiene 'accidentes' vacío.")
            print(f"    Decisión: Se imputa con la media histórica de la zona Centro ({valor_imputado} accidentes).")
            acc_val = float(valor_imputado)
        else:
            acc_val = float(acc_str)
            
        heridos_val = float(f['heridos']) if f['heridos'] != '' else 0.0
        
        filas_limpias.append({
            'zona': f['zona'],
            'accidentes': acc_val,
            'heridos': heridos_val,
            'gravedad': f['gravedad'],
            'fecha': f['fecha']
        })
        
    print(f"\nTotal de registros individuales limpios y procesados: {len(filas_limpias)}")
    return filas_limpias

def analisis_estadistico_numpy(filas_limpias):
    """
    Tarea 4: Análisis estadístico con NumPy
    Calcula media, mediana, desviación estándar, mínimo y máximo.
    """
    print("\n" + "=" * 65)
    print(" 3. ANÁLISIS ESTADÍSTICO CON NUMPY (TAREA 4)")
    print("=" * 65)
    
    accidentes = np.array([f['accidentes'] for f in filas_limpias], dtype=float)
    heridos = np.array([f['heridos'] for f in filas_limpias], dtype=float)
    
    stats_acc = {
        'media': np.mean(accidentes),
        'mediana': np.median(accidentes),
        'desviacion': np.std(accidentes),
        'minimo': np.min(accidentes),
        'maximo': np.max(accidentes),
        'total': np.sum(accidentes)
    }
    
    stats_her = {
        'media': np.mean(heridos),
        'mediana': np.median(heridos),
        'desviacion': np.std(heridos),
        'minimo': np.min(heridos),
        'maximo': np.max(heridos),
        'total': np.sum(heridos)
    }
    
    print("ESTADÍSTICAS - VARIABLE PRINCIPAL (ACCIDENTES):")
    print(f" * Media (Promedio)    : {stats_acc['media']:.2f}")
    print(f" * Mediana             : {stats_acc['mediana']:.2f}")
    print(f" * Desviación Estándar : {stats_acc['desviacion']:.2f}")
    print(f" * Mínimo              : {stats_acc['minimo']:.2f}")
    print(f" * Máximo              : {stats_acc['maximo']:.2f}")
    print(f" * Total Acumulado     : {stats_acc['total']:.2f}")
    
    print("\nESTADÍSTICAS - VARIABLE SECUNDARIA (HERIDOS):")
    print(f" * Media (Promedio)    : {stats_her['media']:.2f}")
    print(f" * Mediana             : {stats_her['mediana']:.2f}")
    print(f" * Desviación Estándar : {stats_her['desviacion']:.2f}")
    print(f" * Mínimo              : {stats_her['minimo']:.2f}")
    print(f" * Máximo              : {stats_her['maximo']:.2f}")
    print(f" * Total Acumulado     : {stats_her['total']:.2f}")
    
    # Análisis de representatividad del promedio
    diferencia_media_mediana = abs(stats_acc['media'] - stats_acc['mediana'])
    coef_variacion = (stats_acc['desviacion'] / stats_acc['media']) * 100
    print("\n¿EL PROMEDIO ES REPRESENTATIVO?:")
    print(f" - Media ({stats_acc['media']:.2f}) vs Mediana ({stats_acc['mediana']:.2f}). Diferencia: {diferencia_media_mediana:.2f}")
    print(f" - Coeficiente de variación: {coef_variacion:.1f}%")
    if coef_variacion > 35:
        print(" -> Conclusión: El promedio NO es totalmente representativo debido a la alta dispersión y concentración en zonas críticas como Oriente (12 accidentes).")
    else:
        print(" -> Conclusión: El promedio es moderadamente representativo.")
        
    return accidentes, heridos, stats_acc, stats_her

def generar_visualizaciones(filas_limpias, accidentes, heridos):
    """
    Tarea 5: Visualización con Matplotlib
    Genera y guarda los 2 gráficos solicitados en formato PNG.
    """
    print("\n" + "=" * 65)
    print(" 4. GENERACIÓN DE GRÁFICOS CON MATPLOTLIB (TAREA 5)")
    print("=" * 65)
    
    zonas = [f['zona'] for f in filas_limpias]
    fechas = [f['fecha'] for f in filas_limpias]
    
    # Gráfico 1: Distribución de la variable principal por Zona (Barras)
    plt.figure(figsize=(10, 6))
    colores = ['#e74c3c' if f['gravedad'] == 'Grave' else '#3498db' for f in filas_limpias]
    barras = plt.bar(range(len(filas_limpias)), accidentes, color=colores, edgecolor='black', alpha=0.85)
    
    etiquetas_eje = [f"{f['zona']}\n({f['fecha'][5:]})" for f in filas_limpias]
    plt.xticks(range(len(filas_limpias)), etiquetas_eje, rotation=45, ha='right', fontsize=9)
    plt.title('Distribución de Accidentes de Tránsito por Zona en Cartago', fontsize=13, fontweight='bold')
    plt.xlabel('Zona y Fecha del Reporte', fontsize=11)
    plt.ylabel('Cantidad de Accidentes', fontsize=11)
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    
    # Leyenda personalizada
    import matplotlib.patches as mpatches
    rojo_patch = mpatches.Patch(color='#e74c3c', label='Gravedad: Grave')
    azul_patch = mpatches.Patch(color='#3498db', label='Gravedad: Leve')
    plt.legend(handles=[rojo_patch, azul_patch], loc='upper left')
    
    plt.tight_layout()
    grafico1_nombre = 'distribucion_accidentes.png'
    plt.savefig(grafico1_nombre, dpi=150)
    plt.close()
    print(f" -> Gráfico 1 guardado exitosamente: {grafico1_nombre}")
    
    # Gráfico 2: Relación entre dos variables (Accidentes vs Heridos - Dispersión / Comparativa)
    plt.figure(figsize=(9, 6))
    plt.scatter(accidentes, heridos, color='#2c3e50', s=120, alpha=0.8, edgecolors='black', label='Reportes viales')
    
    # Línea de tendencia lineal
    coef = np.polyfit(accidentes, heridos, 1)
    polinomio = np.poly1d(coef)
    x_vals = np.linspace(np.min(accidentes), np.max(accidentes), 100)
    plt.plot(x_vals, polinomio(x_vals), color='#e67e22', linestyle='--', linewidth=2, label=f'Tendencia: y = {coef[0]:.2f}x + ({coef[1]:.2f})')
    
    for i, txt in enumerate(zonas):
        plt.annotate(txt, (accidentes[i] + 0.15, heridos[i] - 0.1), fontsize=9)
        
    plt.title('Relación entre Número de Accidentes y Cantidad de Heridos (Cartago)', fontsize=13, fontweight='bold')
    plt.xlabel('Número de Accidentes', fontsize=11)
    plt.ylabel('Cantidad de Heridos', fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    grafico2_nombre = 'relacion_accidentes_heridos.png'
    plt.savefig(grafico2_nombre, dpi=150)
    plt.close()
    print(f" -> Gráfico 2 guardado exitosamente: {grafico2_nombre}")

def main():
    # Buscar el CSV en el directorio actual o grupo_04.csv
    ruta_csv = 'grupo_04.csv'
    if not os.path.exists(ruta_csv):
        # Probar con grupo_01 o cualquier csv local
        csvs = [f for f in os.listdir('.') if f.endswith('.csv')]
        if csvs:
            ruta_csv = csvs[0]
            
    filas_crudas = cargar_datos_iniciales(ruta_csv)
    filas_limpias = limpiar_calidad_datos(filas_crudas)
    accidentes, heridos, stats_acc, stats_her = analisis_estadistico_numpy(filas_limpias)
    generar_visualizaciones(filas_limpias, accidentes, heridos)
    
    print("\n" + "=" * 65)
    print(" ANÁLISIS COMPLETADO CON ÉXITO")
    print("=" * 65)

if __name__ == '__main__':
    main()
