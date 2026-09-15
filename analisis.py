import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def cargar_datos_iniciales(ruta_csv):
    print("=" * 65)
    print(" CARGA DE DATOS INICIALES")
    print("=" * 65)
    
    filas_crudas = []
    with open(ruta_csv, 'r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            filas_crudas.append(fila)
            
    print(f"Total registros leídos: {len(filas_crudas)}")
    print("\nPrimeras 5 filas:")
    print("-" * 65)
    for i, fila in enumerate(filas_crudas[:5], 1):
        print(f"Fila {i}: {fila}")
    print("-" * 65)
    return filas_crudas

def limpiar_calidad_datos(filas_crudas):
    print("\n" + "=" * 65)
    print(" TRATAMIENTO DE DATOS")
    print("=" * 65)
    
    filas_limpias = []
    valores_centro_accidentes = []
    
    for f in filas_crudas:
        if f['zona'] == 'Centro' and f['accidentes'] != '' and f['zona'] != 'RESUMEN':
            valores_centro_accidentes.append(float(f['accidentes']))
            
    valor_imputado = int(np.round(np.mean(valores_centro_accidentes)))
    
    for f in filas_crudas:
        if f['zona'].upper() == 'RESUMEN':
            print(" -> Fila RESUMEN excluida.")
            continue
            
        acc_str = f['accidentes']
        if acc_str == '' or acc_str is None:
            print(f" -> Dato faltante en Centro ({f['fecha']}). Se imputa valor: {valor_imputado}")
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
        
    print(f"\nRegistros procesados: {len(filas_limpias)}")
    return filas_limpias

def analisis_estadistico_numpy(filas_limpias):
    print("\n" + "=" * 65)
    print(" ANÁLISIS ESTADÍSTICO")
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
    
    print("ACCIDENTES:")
    print(f" Media    : {stats_acc['media']:.2f}")
    print(f" Mediana  : {stats_acc['mediana']:.2f}")
    print(f" Desv Std : {stats_acc['desviacion']:.2f}")
    print(f" Minimo   : {stats_acc['minimo']:.2f}")
    print(f" Maximo   : {stats_acc['maximo']:.2f}")
    print(f" Total    : {stats_acc['total']:.2f}")
    
    print("\nHERIDOS:")
    print(f" Media    : {stats_her['media']:.2f}")
    print(f" Mediana  : {stats_her['mediana']:.2f}")
    print(f" Desv Std : {stats_her['desviacion']:.2f}")
    print(f" Minimo   : {stats_her['minimo']:.2f}")
    print(f" Maximo   : {stats_her['maximo']:.2f}")
    print(f" Total    : {stats_her['total']:.2f}")
    
    diferencia = abs(stats_acc['media'] - stats_acc['mediana'])
    cv = (stats_acc['desviacion'] / stats_acc['media']) * 100
    print("\nREPRESENTATIVIDAD:")
    print(f" Media vs Mediana: diff {diferencia:.2f}")
    print(f" Coeficiente de variacion: {cv:.1f}%")
        
    return accidentes, heridos, stats_acc, stats_her

def generar_visualizaciones(filas_limpias, accidentes, heridos):
    print("\n" + "=" * 65)
    print(" GENERACIÓN DE GRÁFICOS")
    print("=" * 65)
    
    zonas = [f['zona'] for f in filas_limpias]
    
    plt.figure(figsize=(10, 6))
    colores = ['#e74c3c' if f['gravedad'] == 'Grave' else '#3498db' for f in filas_limpias]
    plt.bar(range(len(filas_limpias)), accidentes, color=colores, edgecolor='black', alpha=0.85)
    
    etiquetas_eje = [f"{f['zona']}\n({f['fecha'][5:]})" for f in filas_limpias]
    plt.xticks(range(len(filas_limpias)), etiquetas_eje, rotation=45, ha='right', fontsize=9)
    plt.title('Distribución de Accidentes de Tránsito por Zona en Cartago', fontsize=13, fontweight='bold')
    plt.xlabel('Zona y Fecha del Reporte', fontsize=11)
    plt.ylabel('Cantidad de Accidentes', fontsize=11)
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    
    rojo_patch = mpatches.Patch(color='#e74c3c', label='Gravedad: Grave')
    azul_patch = mpatches.Patch(color='#3498db', label='Gravedad: Leve')
    plt.legend(handles=[rojo_patch, azul_patch], loc='upper left')
    
    plt.tight_layout()
    plt.savefig('distribucion_accidentes.png', dpi=150)
    plt.close()
    print(" -> distribucion_accidentes.png generado.")
    
    plt.figure(figsize=(9, 6))
    plt.scatter(accidentes, heridos, color='#2c3e50', s=120, alpha=0.8, edgecolors='black', label='Reportes viales')
    
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
    plt.savefig('relacion_accidentes_heridos.png', dpi=150)
    plt.close()
    print(" -> relacion_accidentes_heridos.png generado.")

def main():
    ruta_csv = 'grupo_04.csv'
    if not os.path.exists(ruta_csv):
        csvs = [f for f in os.listdir('.') if f.endswith('.csv')]
        if csvs:
            ruta_csv = csvs[0]
            
    filas_crudas = cargar_datos_iniciales(ruta_csv)
    filas_limpias = limpiar_calidad_datos(filas_crudas)
    accidentes, heridos, stats_acc, stats_her = analisis_estadistico_numpy(filas_limpias)
    generar_visualizaciones(filas_limpias, accidentes, heridos)
    print("\nProceso finalizado con éxito.")

if __name__ == '__main__':
    main()
