# Primer Parcial - Inteligencia Artificial

**Integrantes:** Brandon Cortes Giraldo — Johan Sttive Linares Barragán  
**Grupo:** 04  
**Docente:** Jhon James Cano Sánchez  
**Institución:** COTECNOVA - Cartago, Valle  

---

## 1. Configuración del Entorno

El proyecto se configuró con Docker y WSL 2 usando Python 3.12, NumPy y Matplotlib.

Para ejecutarlo con Docker:
```bash
docker compose up --build
```

O directamente en terminal local:
```bash
python3 analisis.py
```

---

## 2. Carga de Datos

El script `analisis.py` lee el archivo `grupo_04.csv` con `csv.DictReader`.
* **Total de filas leídas:** 12 registros.
* **Columnas:** `zona`, `accidentes`, `heridos`, `gravedad`, `fecha`.

---

## 3. Calidad de Datos

Al revisar el CSV encontramos 3 problemas puntuales:

1. **Fila RESUMEN (Fila 12):**
   * *Detección:* Aparece como una zona llamada "RESUMEN" con totales acumulados (62 accidentes, 42 heridos) y campos vacíos en fecha y gravedad.
   * *Decisión:* Se eliminó del análisis.
   * *Por qué:* No es un evento individual. Si se deja, duplica los datos y altera la media y la desviación.

2. **Dato faltante en accidentes (Fila 11 - Centro, 2026-06-01):**
   * *Detección:* La celda de accidentes venía vacía, pero reportaba 1 herido.
   * *Decisión:* Se imputó con 4 accidentes (el promedio de los otros registros del Centro: 5 y 4).
   * *Por qué:* Como hubo 1 herido, no podía ser 0. Descartar la fila borraba el registro del herido, así que se usó la media de esa misma zona.

3. **Inconsistencia en la suma del resumen:**
   * *Detección:* La suma de las primeras 10 filas daba exactamente 62, lo que evidenció que la fila 11 no se había sumado en el resumen original.
   * *Decisión:* Recalcular los totales desde los datos limpios.
   * *Por qué:* Para trabajar con el total real (66 accidentes y 42 heridos) y no con un error de digitación.

* **Pregunta clave:** El valor más sospechoso era la fila RESUMEN. Si no se quita, infla el total de accidentes a 128 y distorsiona cualquier decisión que tome la alcaldía.

---

## 4. Análisis Estadístico con NumPy

Cálculos sobre los 11 registros limpios:

| Métrica | Accidentes | Heridos |
|---|---|---|
| Media | 6.00 | 3.82 |
| Mediana | 5.00 | 3.00 |
| Desviación estándar | 2.89 | 2.79 |
| Mínimo | 2.00 (Sur) | 0.00 (Sur) |
| Máximo | 12.00 (Oriente) | 9.00 (Oriente) |
| Total real | 66 | 42 |

* **¿El promedio es representativo?:**  
  No del todo. El coeficiente de variación es del **48.2%** (desviación de 2.89 sobre media de 6.00), lo que indica datos dispersos. Zonas como Oriente (12 y 10 accidentes) suben el promedio, mientras que en el Sur solo hay 2 o 3. La **mediana (5.0)** refleja mejor un valor típico.

---

## 5. Visualizaciones (Matplotlib)

1. **`distribucion_accidentes.png`:** Gráfico de barras por zona y fecha. Muestra claramente que los accidentes graves se concentran en Oriente (12 y 10) y Norte (8 y 7), mientras que Centro, Sur y Occidente tuvieron accidentes leves.
2. **`relacion_accidentes_heridos.png`:** Gráfico de dispersión. Muestra una relación directa entre las dos variables: a mayor cantidad de accidentes en la zona, mayor es el número de heridos reportados.

---

## 6. Interpretación de los Datos

* **Relación:** Hay correlación positiva clara entre accidentes y heridos. La gravedad se relaciona con el tipo de vía: en Oriente y Norte son vías más rápidas con choques más fuertes, mientras que en el Centro el tráfico lento genera choques leves.
* **Situación en Cartago:** La accidentalidad grave está focalizada en las salidas y corredores del Oriente y Norte de la ciudad, no en toda la ciudad por igual.
* **Patrón no evidente:** El Sur presenta cifras muy bajas (solo 1 herido en total), lo que puede indicar menor flujo vehicular o posibles casos no reportados formalmente.

---

## 7. Recomendaciones para Cartago

1. **Controles en Oriente:** Instalar reductores y cámaras en la zona Oriente, ya que concentró **22 accidentes y 17 heridos** (el **33.3%** de los accidentes y el **40.5%** de los heridos de todo el dataset).
2. **Reubicar agentes:** Mover personal de tránsito desde el Sur (donde solo hubo **5 accidentes y 1 herido**) hacia el Norte (**15 accidentes y 11 heridos graves**).
3. **Atención médica:** Ubicar ambulancias cerca de los corredores viales de Oriente y Norte para atender más rápido los choques de alta gravedad.

---

## 8. Limitaciones

* Son solo 11 registros en un lapso de 6 meses, lo que no permite ver patrones por días de la semana ni por horas pico.
* No se especifica si los accidentes fueron en moto o en carro.
* Para un modelo de IA más adelante se necesitarían coordenadas GPS exactas, horas del día y causas probables del accidente.
