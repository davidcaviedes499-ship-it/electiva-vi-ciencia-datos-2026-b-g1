# Parcial Práctico · Corte 1
## Analítica de datos aplicada al diagnóstico automotriz

**Autor:** David Caviedes
**Facultad de Ingeniería, Corporación Universitaria del Huila (CORHUILA)**
**Asignatura: Ciencia de Datos · Corte 1 · Periodo 2026-B**
**Septiembre de 2026**

---

## Caso seleccionado: diagnóstico de fallas electrónicas en vehículos

El diagnóstico electrónico automotriz es un proceso en el que se recopilan y comparan datos provenientes de diferentes fuentes del vehículo. Entre ellos se encuentran los códigos de diagnóstico (DTC), las revoluciones del motor, temperaturas, presiones, voltajes, información de las unidades de control electrónico, registros del escáner, antecedentes de mantenimiento y observaciones realizadas durante la revisión. La combinación de estas evidencias permite organizar el proceso de diagnóstico y evita depender únicamente de un código de falla aislado.

Desde la perspectiva de la ciencia de datos, este caso es útil porque integra información con diferentes niveles de estructura: valores numéricos que pueden almacenarse directamente en tablas, campos o metadatos que pueden variar según la herramienta utilizada, y evidencias como fotografías o descripciones libres que no siguen un esquema tabular fijo.

---

## 1. Identificación y clasificación de los datos

Se seleccionaron cuatro tipos de datos representativos del proceso de diagnóstico electrónico, clasificados según la forma en que cada uno puede almacenarse y organizarse:

| # | Tipo de dato | Ejemplo | Clasificación | Justificación |
|---|---|---|---|---|
| 1 | Códigos de diagnóstico (DTC) | P0300, P0299 o P0101 | **Estructurado** | Son códigos alfanuméricos que pueden almacenarse en campos definidos junto con fecha, vehículo y condición de prueba. |
| 2 | Revoluciones del motor (RPM) | 850 RPM | **Estructurado** | Es una medición numérica con una unidad definida que puede organizarse fácilmente en filas y columnas. |
| 3 | Registros del escáner | Log con PID, tiempo y valor | **Semiestructurado** | Puede contener campos, etiquetas y metadatos identificables, aunque su organización puede variar según el escáner o el formato utilizado. |
| 4 | Fotografías del diagnóstico | ECU, conectores, cableado o componentes | **No estructurado** | El contenido visual no sigue un esquema tabular fijo y requiere interpretación para extraer información útil. |

Los códigos DTC y las RPM se consideran datos estructurados porque pueden representarse mediante campos previamente definidos (código, valor medido, unidad, fecha y condiciones de la prueba), lo que facilita su almacenamiento, filtrado y comparación. Los registros del escáner se consideran semiestructurados porque contienen identificadores de parámetros, marcas de tiempo y valores, pero su formato puede cambiar entre herramientas. Las fotografías son no estructuradas porque representan evidencia visual que no está organizada originalmente como tabla de valores.

---

## 2. Analítica descriptiva y analítica predictiva

La analítica descriptiva permite resumir lo que ocurrió o lo que se ha observado en los datos disponibles. En un taller puede utilizarse para conocer cuáles códigos aparecen con mayor frecuencia, qué valores de operación fueron registrados o qué tipos de fallas se repiten en los vehículos atendidos.

**Pregunta de analítica descriptiva:**
> ¿Cuáles son los códigos DTC y los valores de RPM, voltaje y temperatura que aparecen con mayor frecuencia en los diagnósticos registrados?

La analítica predictiva, en cambio, busca estimar qué podría ocurrir posteriormente utilizando información histórica. En el caso automotriz, una base de datos suficientemente amplia podría relacionar antecedentes de mantenimiento, DTC, kilometraje y mediciones para estimar la probabilidad de recurrencia de determinadas fallas.

**Pregunta de analítica predictiva:**
> ¿Qué vehículos presentan mayor probabilidad de repetir una falla electrónica a partir de sus DTC, mediciones e historial de mantenimiento?

---

## 3. Flujo de datos: Fuente → Almacenamiento → Análisis → Visualización

![Flujo de datos aplicado al diagnóstico electrónico de fallas en vehículos](./diagrama-flujo-datos.png)

*Figura 1. Flujo de datos aplicado al diagnóstico electrónico de fallas en vehículos.*

**Fuente.** Los datos pueden provenir del escáner OBD-II, sensores, unidades de control electrónico, instrumentos de medición, historial de mantenimiento, observaciones del cliente y evidencia visual. Cada fuente aporta una parte diferente de la condición del vehículo.

**Almacenamiento.** La información recopilada puede conservarse en una base de datos o registros del taller. Allí pueden organizarse los DTC, parámetros medidos, logs del escáner, historiales de servicio y archivos asociados al diagnóstico.

**Análisis.** Los datos almacenados pueden utilizarse para resumir fallas frecuentes, comparar mediciones, identificar patrones y relacionar diferentes variables. Con suficiente historial, estos datos también podrían utilizarse para desarrollar modelos predictivos.

**Visualización.** Los resultados del análisis pueden mostrarse mediante tablas, gráficas, indicadores o reportes por vehículo, lo que facilita que el técnico interprete los resultados antes de tomar una decisión.

---

## 4. Descriptive Analytics vs. Predictive Analytics (English)

Descriptive analytics uses historical data to understand what happened in previous vehicle diagnostics. Predictive analytics uses historical data and models to estimate what may happen in future vehicle diagnostics.

---

## Conclusión

El diagnóstico electrónico de vehículos es un caso apropiado para aplicar conceptos básicos de analítica de datos porque reúne información numérica, registros técnicos y evidencia visual. Clasificar correctamente los datos permite comprender cómo deben almacenarse y procesarse. La analítica descriptiva ayuda a resumir los diagnósticos realizados, mientras que la analítica predictiva podría utilizar el historial acumulado para estimar la recurrencia de determinadas fallas. El flujo Fuente → Almacenamiento → Análisis → Visualización muestra de forma sencilla cómo la información puede transformarse desde su obtención hasta su presentación para apoyar el proceso técnico.

---

## Referencias

- IBM. (2024). *Structured vs. unstructured data: What's the difference?* IBM Think.
- IBM. (2022). *What is predictive analytics?* IBM Think.
- U.S. Environmental Protection Agency. (2018). *OBDII test procedures*. EPA.
