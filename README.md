# Primer Parcial - Inteligencia Artificial (COTECNOVA 2026)

**Estudiante:** Brandon Cortes Giraldo  
**Grupo Asignado:** Grupo 04  
**Docente:** Jhon James Cano Sánchez  
**Materia:** Inteligencia Artificial  
**Institución:** Corporación de Estudios Tecnológicos del Norte del Valle (COTECNOVA)  
**Ciudad:** Cartago, Valle del Cauca  

---

## 1. Configuración del Entorno de Desarrollo

El proyecto está configurado para ejecutarse en un entorno reproducible utilizando **Docker**, **Docker Compose** y **WSL 2 (Ubuntu)** con Python 3.12, NumPy y Matplotlib.

### Pasos para reproducir y ejecutar el entorno:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Brandon07-code/Parcial-Curso-IA.git
   cd Parcial-Curso-IA
   ```

2. **Construir y levantar el contenedor con Docker Compose:**
   ```bash
   docker compose up --build
   ```

3. **Ejecución alternativa directamente en WSL / Terminal:**
   ```bash
   python3 analisis.py
   ```

---

## 2. Carga y Estructura de Datos

Se implementó el script `analisis.py` que lee el archivo asignado `grupo_04.csv` mediante la biblioteca estándar `csv.DictReader`.

* **Número total de registros brutos:** 12 registros leídos.
* **Estructura de columnas:**
  * `zona`: Sector geográfico de Cartago (Centro, Norte, Sur, Oriente, Occidente).
  * `accidentes`: Número de siniestros viales reportados.
  * `heridos`: Número de personas lesionadas.
  * `gravedad`: Nivel cualitativo del siniestro (Leve, Grave).
  * `fecha`: Fecha del registro temporal (formato AAAA-MM-DD).

---

## 3. Calidad de Datos

Durante la auditoría inicial del dataset se detectaron **tres (3) problemas críticos de calidad de datos**:

### Problema 1: Fila de Resumen en medio de datos tabulares (Fila 12: `RESUMEN`)
* **¿Cómo se detectó?:** Al inspeccionar los valores únicos de la columna `zona`, se encontró el valor `"RESUMEN"`, el cual presentaba valores agregados (62 accidentes, 42 heridos) y campos vacíos en `gravedad` y `fecha`.
* **¿Qué decisión se tomó?:** Se filtró y excluyó esta fila del análisis estadístico por registro individual.
* **¿Por qué se tomó esa decisión?:** En bases de datos y ciencia de datos, mezclar filas totalizadoras con registros atómicos duplica artificialmente las métricas de tendencia central y dispersión (media, mediana y varianza).

### Problema 2: Dato Faltante (Valor Nulo) en la variable `accidentes` (Fila 11: Centro, 2026-06-01)
* **¿Cómo se detectó?:** Mediante validación de cadenas vacías (`acc_str == ''`), identificando que el registro del 1 de junio en el Centro carecía de cantidad de accidentes pero registraba `1 herido`.
* **¿Qué decisión se tomó?:** Se realizó una **imputación estadística** asignando el valor **4** (la media/mediana histórica de la zona Centro, cuyos reportes previos fueron 5 y 4).
* **¿Por qué se tomó esa decisión?:** Eliminar la fila completa provocaría la pérdida de información sobre el herido registrado en esa fecha. Además, como hay 1 persona lesionada, es matemáticamente imposible que hubiera 0 accidentes. Imputar con la tendencia de la misma zona mantiene la consistencia biológica y operativa del dataset.

### Problema 3: Inconsistencia lógica entre la suma de registros y la fila de resumen
* **¿Cómo se detectó?:** La suma manual de las primeras 10 filas de accidentes daba exactamente `62`, que coincide con el valor de la fila `RESUMEN`, lo que evidencia que la fila 11 (incompleta) no fue tenida en cuenta en el resumen original del archivo.
* **¿Qué decisión se tomó?:** Recalcular todas las métricas agregadas directamente sobre los registros limpios e imputados (obteniendo un total real de **66 accidentes** y **42 heridos**).
* **¿Por qué se tomó esa decisión?:** Evita confiar en agregaciones manuales previas con errores de digitación y garantiza integridad en el diagnóstico municipal.

### Pregunta Clave de Calidad:
> *¿Hay algún valor en los datos que le parezca sospechoso o inconsistente? ¿Cómo afecta el análisis si no se corrige?*  
> **Respuesta:** La fila `RESUMEN` es el valor más peligroso. Si no se elimina, el total de accidentes pasaría erróneamente de 66 a 128, y el promedio de accidentes se duplicaría artificialmente, llevando a la Secretaría de Tránsito de Cartago a sobreestimar el presupuesto de intervención en más de un 100%.

---

## 4. Análisis Estadístico con NumPy

Utilizando arrays vectorizados de **NumPy**, se obtuvieron las siguientes métricas sobre los registros individuales limpios:

| Métrica | Variable Principal: `accidentes` | Variable Secundaria: `heridos` |
|---|---|---|
| **Media (Promedio)** | **6.00** | **3.82** |
| **Mediana** | **5.00** | **3.00** |
| **Desviación Estándar ($\sigma$)** | **2.89** | **2.79** |
| **Valor Mínimo** | **2.00** (Sur) | **0.00** (Sur) |
| **Valor Máximo** | **12.00** (Oriente) | **9.00** (Oriente) |
| **Suma Total Real** | **66.00** | **42.00** |

### Pregunta Clave: ¿El promedio es representativo de los datos?
> **Respuesta:** **El promedio NO es totalmente representativo.**  
> **Justificación numérica:**
> 1. Existe una brecha de **1.0 unidad** entre la media (6.00) y la mediana (5.00), lo que indica asimetría positiva hacia la derecha.
> 2. El **Coeficiente de Variación ($CV = \frac{\sigma}{\mu}$)** es del **$48.17\%$** ($\frac{2.89}{6.00} \times 100$). En estadística, un coeficiente de variación superior al 30% demuestra **alta heterogeneidad y dispersión**.
> 3. Los valores extremos de la zona Oriente (**12** y **10** accidentes) elevan artificialmente la media, mientras que zonas como el Sur registran apenas **2** y **3** accidentes. Por lo tanto, la **mediana (5.0)** representa con mayor fidelidad el comportamiento típico de una zona en Cartago.

---

## 5. Visualizaciones Generadas (Matplotlib)

El script generó y guardó dos gráficos en formato `.png`:

### Gráfico 1: `distribucion_accidentes.png`
* **Tipo:** Gráfico de barras por zona y fecha, coloreado según nivel de gravedad (Rojo: Grave, Azul: Leve).
* **Interpretación:** Permite visualizar de inmediato que la accidentalidad no es homogénea en Cartago. La zona **Oriente** (barras rojas más altas con 12 y 10 siniestros) y la zona **Norte** (8 y 7 siniestros) concentran todos los accidentes calificados como **Graves**, mientras que Centro, Occidente y Sur registran niveles Leves.

### Gráfico 2: `relacion_accidentes_heridos.png`
* **Tipo:** Gráfico de dispersión con línea de tendencia lineal ajustada.
* **Interpretación:** Demuestra una **fuerte correlación lineal positiva** entre el número de accidentes y el número de lesionados ($y \approx 0.92x - 1.7$). A mayor número de siniestros en una zona, el número de heridos escala de forma proporcional y directa, alcanzando su punto crítico en la zona Oriente con 9 heridos en un solo reporte.

---

## 6. Interpretación Profunda

1. **¿Qué relación existe entre las variables? ¿Hay correlación? ¿Es causalidad?:**  
   Existe una **alta correlación estadística positiva** entre siniestros y heridos. Sin embargo, no todo accidente causa víctimas mortales o heridos de gravedad; la variable cualitativa `gravedad` revela que la gravedad está asociada a la **velocidad y tipología de vía** de cada zona (e.g. vías rápidas en el Oriente/Norte de Cartago frente a vías lentas y congestionadas del Centro).
2. **¿Qué historia cuentan los datos sobre Cartago?:**  
   Los datos muestran una marcada brecha territorial: el **Oriente y el Norte representan el epicentro de la accidentalidad severa** de la ciudad, mientras que el Centro presenta choques frecuentes pero de baja lesividad (choques simples en semáforos o cruces urbanos).
3. **Patrones no evidentes a simple vista:**  
   El sector Sur presenta una tasa de lesividad casi nula (0 y 1 herido), lo que sugiere zonas residenciales de tráfico calmado o un subregistro de accidentes menores no reportados formalmente.

---

## 7. Recomendaciones Basadas en Evidencia

Para la Secretaría de Movilidad y la Alcaldía Municipal de Cartago se formulan las siguientes recomendaciones basadas en datos:

1. **Focalización Operativa en el Oriente y Norte:** Instalar reductores de velocidad, cámaras de fotodetección y puestos de control fijos en los corredores viales de la zona Oriente, ya que en solo dos registros acumuló **22 accidentes y 17 heridos** (representando el **$33.3\%$** de los siniestros y el **$40.5\%$** de todas las víctimas de la ciudad).
2. **Reorganización de Cuadrillas de Agentes de Tránsito:** Reasignar el personal operativo desde zonas de bajo impacto como el Sur (donde solo hubo **5 accidentes acumulados y 1 herido**) hacia las comunas de la zona Norte (**15 accidentes y 11 heridos graves**).
3. **Plan de Atención Prehospitalaria Rápida:** Posicionar ambulancias medicalizadas estratégicamente en el perímetro Oriente-Norte, garantizando respuesta en menos de 7 minutos ante siniestros de alta cinemática.

---

## 8. Limitaciones del Dataset

1. **Muestra Temporal Reducida:** El dataset contiene solo 11 observaciones distribuidas en 6 meses, lo que impide evaluar estacionalidad climática (épocas de lluvias intensas en Cartago) o patrones por horas del día (horas pico vs madrugada).
2. **Falta de Variables Cruciales:** No se dispone del tipo de vehículo involucrado (motocicletas vs automóviles), estado de la malla vial (huecos o pavimento mojado) ni causa probable del siniestro (embriaguez, exceso de velocidad o imprudencia).
3. **Datos adicionales requeridos para un modelo predictivo de IA:**
   * Coordenadas GPS exactas para mapas de calor geográficos (GIS).
   * Horario exacto y día de la semana.
   * Aforo vehicular promedio por corredor vial de Cartago.
