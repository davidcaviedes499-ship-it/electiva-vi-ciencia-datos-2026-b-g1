# 🚗🔍 DIAGNÓSTICO DE DATOS DE UN PROCESO
## ⚙️ Diagnóstico de fallas electrónicas en vehículos mediante análisis de datos
**Actividad calificable · Corte 1 — Ciencia de Datos**

*Un enfoque de ciencia de datos aplicado al diagnóstico electrónico automotriz.*

🚘 **Vehículo** → 🔌 **Datos** → 🔍 **Análisis** → 🧠 **Diagnóstico** → 🛠️ **Decisión**

---

**David Caviedes**  
Facultad de Ingeniería  
Corporación Universitaria del Huila (CORHUILA)  
Asignatura: Ciencia de Datos  
Unidad 1: Fundamentos de Ciencia de Datos y Big Data  
Periodo: 2026-B  
Fecha: Agosto de 2026

---

## 📑 Tabla de contenido

- Abstract
- 1. Introducción
- 2. Objetivos
- 3. Marco teórico
- 4. Planteamiento del problema
- 5. Problem & data
- 6. Inventario de datos
- 7. Tipo de analítica aplicada
- 8. ¿Es un caso de Big Data?
- 9. Ciclo de vida del proyecto
- 10. Conclusiones
- 11. Referencias

---

## 🌎 Abstract

This report presents a data diagnosis applied to a real automotive process: electronic vehicle fault diagnosis. The purpose is to determine how information obtained from on-board diagnostic systems, electronic control units, sensors, measurements, maintenance records and customer observations can be organized and analyzed to support the identification of a probable fault cause. The project classifies the available information into structured, semi-structured and unstructured data, selects diagnostic analytics as the main analytical approach, and evaluates the case using the five V's of Big Data: volume, velocity, variety, veracity and value. The complete data life cycle — question, obtain, clean, analyze, visualize and decide — is then applied to the diagnostic process. The proposed approach does not replace technical testing; instead, it organizes evidence so that diagnostic decisions can be more systematic and traceable.

**Keywords:** data science, automotive diagnostics, OBD-II, diagnostic analytics, Big Data, DTC.

---

## 1. 📘 Introducción

El diagnóstico electrónico automotriz es un proceso en el que se recopilan y contrastan datos provenientes de diferentes fuentes del vehículo. Los sistemas OBD permiten recuperar información como el estado de la lámpara MIL, códigos de diagnóstico (DTC), monitores de preparación y otros datos del sistema. La Agencia de Protección Ambiental de Estados Unidos (EPA) explica que, cuando el sistema OBD detecta determinadas fallas, puede almacenar un DTC y condiciones de operación en la memoria del módulo de control [1].

En un taller, sin embargo, la lectura de un código no constituye por sí sola una conclusión sobre la pieza que debe reemplazarse. El diagnóstico puede requerir relacionar códigos, parámetros en vivo, voltajes, presiones, temperaturas, revoluciones, antecedentes de mantenimiento, síntomas descritos por el cliente y evidencia visual. Desde la perspectiva de ciencia de datos, esto convierte el diagnóstico en un problema interesante porque combina información con distintos niveles de estructura y calidad.

Este trabajo propone un diagnóstico de datos del proceso de identificación de fallas electrónicas en vehículos. El objetivo no es construir todavía un algoritmo automático de reparación, sino definir la pregunta de datos, inventariar las fuentes, establecer el tipo de analítica apropiado, evaluar si el caso corresponde a Big Data y representar el ciclo de vida que transforma datos de diagnóstico en una decisión técnica.

---

## 2. 🎯 Objetivos

### 2.1 🏁 Objetivo general

Diagnosticar la estructura, utilidad y tratamiento de los datos disponibles durante el proceso de diagnóstico electrónico automotriz, con el fin de establecer cómo pueden apoyar la identificación de la causa probable de una falla y orientar las pruebas de reparación.

### 2.2 📌 Objetivos específicos

- Formular una pregunta de datos clara y aplicable al proceso real de diagnóstico electrónico de un vehículo.
- Elaborar un inventario de al menos seis fuentes o campos y clasificarlos como estructurados, semiestructurados o no estructurados.
- Determinar qué tipos de analítica — descriptiva, diagnóstica, predictiva y prescriptiva — pueden aplicarse al proceso y justificar el enfoque principal.
- Evaluar el caso mediante las cinco V de Big Data: volumen, velocidad, variedad, veracidad y valor.
- Representar el ciclo de vida pregunta → obtener → limpiar → analizar → visualizar → decidir aplicado al diagnóstico automotriz.

---

## 3. 📚 Marco teórico

### 3.1 🧠 Ciencia de datos y ciclo de vida

La ciencia de datos busca convertir datos en información útil para comprender fenómenos y apoyar decisiones. En esta actividad se adopta el ciclo definido por el enunciado: pregunta, obtener, limpiar, analizar, visualizar y decidir. Cada etapa cumple una función concreta: formular la necesidad, recopilar evidencia, mejorar su calidad, encontrar relaciones, comunicar resultados y finalmente tomar una decisión.

### 3.2 🗂️ Datos estructurados, semiestructurados y no estructurados

IBM distingue los datos según su esquema. Los datos estructurados siguen un formato predefinido y se organizan fácilmente en filas y columnas. Los datos semiestructurados no siguen un esquema rígido, pero incorporan metadatos, etiquetas o marcadores que facilitan su organización. Los datos no estructurados carecen de un esquema predefinido e incluyen, por ejemplo, texto libre, imágenes, audio y video [2].

### 3.3 📊 Tipos de analítica

IBM resume cuatro tipos principales de analítica: descriptiva (¿qué pasó?), diagnóstica (¿por qué pasó?), predictiva (¿qué podría pasar después?) y prescriptiva (¿qué deberíamos hacer?) [3]. En el caso seleccionado, la analítica diagnóstica es la más importante porque el objetivo central es encontrar causas probables a partir de evidencias.

### 3.4 🌐 Big Data y las cinco V

IBM caracteriza Big Data mediante cinco dimensiones: volumen, velocidad, variedad, veracidad y valor. El volumen se refiere a la cantidad; la velocidad, al ritmo de llegada y procesamiento; la variedad, a los formatos; la veracidad, a la confiabilidad; y el valor, al beneficio que puede obtenerse del análisis [4].

### 3.5 🚘 Diagnóstico a bordo OBD-II

La EPA describe OBD como un sistema computarizado de monitoreo y detección de fallas relacionado con el control de emisiones y la operación del tren motriz. En procedimientos OBD-II se recuperan datos como DTC, estado de MIL y monitores; además, documentación regulatoria de EPA enumera variables diagnósticas como temperatura de refrigerante, presión de admisión, RPM, posición del acelerador y velocidad del vehículo [1], [5].

---

## 4. ⚠️ Planteamiento del problema

### 4.1 🔧 Contexto del proceso

Cuando un vehículo presenta una falla electrónica, el técnico recibe información procedente de varias fuentes. El escáner puede mostrar DTC y parámetros en vivo; el multímetro u otros instrumentos aportan mediciones; el cliente describe síntomas; y el historial de reparaciones aporta antecedentes. Estos datos pueden ser correctos, incompletos, inconsistentes o estar tomados bajo condiciones diferentes.

### 4.2 🧩 Formulación del problema

El problema consiste en organizar y relacionar la evidencia disponible para evitar decisiones basadas únicamente en un código o en una observación aislada. Una misma manifestación puede requerir verificar alimentación eléctrica, señal, comunicación, condiciones de operación o antecedentes antes de establecer una causa probable.

### 4.3 ❓ Pregunta de datos

¿Cómo se pueden analizar los datos obtenidos durante el diagnóstico electrónico de un vehículo para identificar la causa probable de una falla y apoyar la decisión de reparación?

### 4.4 💡 Relevancia del problema

- Reduce la dependencia de decisiones basadas en una sola evidencia.
- Permite documentar y comparar mediciones tomadas durante el diagnóstico.
- Facilita identificar datos faltantes o inconsistentes antes de reemplazar componentes.
- Puede generar una base histórica que, a futuro, permita desarrollar modelos predictivos.

### 4.5 ✅ Decisión que habilita el resultado

El resultado del análisis debe apoyar una decisión técnica concreta: determinar qué prueba realizar a continuación, qué sistema requiere verificación adicional y cuál es la causa probable que cuenta con mayor respaldo en los datos disponibles. La decisión final de reparación debe confirmarse mediante pruebas técnicas.

---

## 5. 🇬🇧 Problem & data

Electronic vehicle diagnosis requires information from several sources, including the on-board diagnostic system, sensors, electronic control units and technician measurements. The main problem is to identify the probable cause of a vehicle fault by combining evidence instead of relying on a single diagnostic trouble code. The required data can include DTCs, engine speed, temperatures, pressures, battery voltage, scanner logs, maintenance records and symptoms reported by the customer. Diagnostic analytics is the main approach because the objective is to understand why the failure is occurring and which variables are related to it. Descriptive analytics can summarize the current condition, while historical records could later support predictive models. The final analysis should help the technician choose the next diagnostic test and make a better supported repair decision.

---

## 6. 🗃️ Inventario de datos

El inventario reúne once fuentes o campos potenciales. La clasificación se realiza por la forma en que el dato se almacena y organiza, siguiendo las definiciones de IBM [2].

| N.º | Fuente / campo | Ejemplo | Tipo | Justificación |
|-----|----------------|---------|------|---------------|
| 1 | Códigos de diagnóstico (DTC) | P0300, P0299, P0101 | Estructurado | Código alfanumérico almacenado por el sistema. |
| 2 | Revoluciones del motor | 850 RPM | Estructurado | Valor numérico con unidad definida. |
| 3 | Temperatura del motor | 92 °C | Estructurado | Medición numérica del parámetro. |
| 4 | Voltaje de batería | 12.6 V | Estructurado | Medición numérica. |
| 5 | Presión del múltiple (MAP) | 45 kPa | Estructurado | Valor numérico obtenido del sistema/sensor. |
| 6 | Registros del escáner | Log con PID, tiempo y valor | Semiestructurado | Puede contener campos y metadatos, pero variar por herramienta/formato. |
| 7 | Información de ECU | ID, versión, calibración | Semiestructurado | Conjunto de campos de identificación y configuración. |
| 8 | Historial de mantenimiento | Fecha, servicio, observación | Semiestructurado | Combina campos repetibles con observaciones variables. |
| 9 | Descripción del cliente | "Pierde potencia al acelerar" | No estructurado | Texto libre. |
| 10 | Fotografías | ECU, conectores, cableado | No estructurado | Contenido visual sin esquema tabular. |
| 11 | Video o audio de la falla | Ruido, vibración, comportamiento | No estructurado | Contenido multimedia. |

### 6.1 🧾 Justificación de la clasificación

Los DTC y las mediciones numéricas se consideran estructurados porque pueden almacenarse con campos definidos: código, valor, unidad, fecha y condición de prueba. Los logs, datos de identificación de ECU e historiales pueden considerarse semiestructurados cuando conservan etiquetas o campos identificables, pero su contenido y formato varían entre herramientas o registros. Las descripciones libres, fotografías, audios y videos son no estructurados porque no siguen un esquema tabular fijo [2].

### 6.2 🧱 Diagrama del inventario

| Estructurados | Semiestructurados | No estructurados |
|---------------|-------------------|------------------|
| DTC | Logs del escáner | Descripción del cliente |
| RPM | Información de ECU | Fotografías |
| Temperatura | Historial de mantenimiento | Videos / audios |
| Voltaje de batería | Organización flexible | Sin esquema fijo |
| Presión MAP | Metadatos/campos identificables | Texto, imagen y multimedia |
| Formato definido / filas y campos repetibles | Requieren interpretación del formato | Requieren extracción/interpretación |

---

## 7. 📈 Tipo de analítica aplicada

| Tipo | Pregunta | Aplicación | Justificación |
|------|----------|------------|---------------|
| Descriptiva | ¿Qué pasó / qué está pasando? | Sí — apoyo | Resume DTC, RPM, voltajes, temperaturas, presiones y otros parámetros. |
| Diagnóstica | ¿Por qué pasó? | Sí — **principal** | Relaciona síntomas, códigos y mediciones para buscar la causa probable. |
| Predictiva | ¿Qué podría pasar? | Potencial | Con una base histórica suficiente podría estimar probabilidad de fallas o recurrencia. |
| Prescriptiva | ¿Qué debería hacerse? | Potencial | Podría recomendar la siguiente prueba o acción según reglas y resultados previos. |

### 7.1 🔎 Analítica seleccionada

La analítica diagnóstica es el enfoque principal. IBM la define como el análisis orientado a descubrir causas raíz, brechas de desempeño y patrones que expliquen por qué ocurrió un resultado [3]. En este proyecto, la pregunta no es únicamente qué DTC está presente, sino qué combinación de datos respalda una causa probable.

---

## 8. 🌐 ¿Es un caso de Big Data?

En la escala de un taller individual, el proceso propuesto no se clasifica necesariamente como Big Data. IBM define Big Data como conjuntos masivos y complejos que los sistemas tradicionales no pueden manejar adecuadamente [4]. Aun así, el caso presenta varias características de las cinco V y podría evolucionar a un escenario de Big Data si se integraran datos continuos de grandes flotas o de miles de vehículos.

| V | Nivel | Aplicación al caso |
|---|-------|--------------------|
| Volumen | Bajo / medio | Un taller puede almacenar muchos diagnósticos, pero normalmente el volumen sigue siendo manejable con herramientas convencionales. |
| Velocidad | Media | Algunos parámetros se generan continuamente durante la operación y pueden muestrearse varias veces por segundo. |
| Variedad | Alta | Se combinan números, códigos, logs, texto libre, fotografías, audio y video. |
| Veracidad | Alta importancia | Una lectura puede estar afectada por condiciones de prueba, sensores defectuosos, mala conexión o datos incompletos; por ello se requiere validación. |
| Valor | Alto | La organización de los datos puede reducir pruebas innecesarias, mejorar la trazabilidad y apoyar decisiones de reparación. |

### 8.1 🧠 Conclusión sobre Big Data

El caso no se considera Big Data por su escala actual. La variedad y la veracidad son las dimensiones más relevantes, mientras que el volumen todavía no exige infraestructura distribuida. Si el proyecto recibiera telemetría continua de una gran flota, aumentaría el volumen y la velocidad, y podría requerir tecnologías de Big Data.

---

## 9. 🔄 Ciclo de vida del proyecto

| Etapa | Aplicación al caso | Herramientas / fuentes |
|-------|--------------------|------------------------|
| 1. Pregunta | ¿Cuál es la causa probable de la falla y qué datos permiten sustentarla? | Definición del problema y síntomas. |
| 2. Obtener | Recopilar DTC, datos en vivo, mediciones, historial, síntomas, imágenes y registros. | Escáner OBD, instrumentos, entrevista, historial. |
| 3. Limpiar | Eliminar duplicados, revisar unidades, identificar datos faltantes y validar condiciones de medición. | Reglas de calidad y validación. |
| 4. Analizar | Relacionar DTC, síntomas y parámetros; comparar valores y buscar patrones o inconsistencias. | Tablas, filtros, análisis diagnóstico. |
| 5. Visualizar | Presentar tendencias, comparaciones y valores anormales de manera comprensible. | Tablas, gráficas, reportes. |
| 6. Decidir | Seleccionar la siguiente prueba y establecer una causa probable respaldada por evidencia. | Decisión técnica y confirmación. |

### 9.1 🧭 Diagrama del ciclo de vida

```
Pregunta
   ↓
Obtener
   ↓
Limpiar
   ↓
Analizar
   ↓
Visualizar
   ↓
Decidir
```

*Ciclo de vida del diagnóstico de falla. Elaboración propia, asistida con IA (ChatGPT).*

El ciclo es iterativo: si durante el análisis aparecen datos inconsistentes o insuficientes, el proceso puede regresar a la etapa de obtener o limpiar. Asimismo, una decisión técnica puede generar nuevas mediciones que alimenten nuevamente el análisis.

### 🔧 Ruta práctica del diagnóstico

```
🚗 Recepción del vehículo
         ↓
💬 Síntomas reportados
         ↓
🔌 Lectura OBD-II / DTC
         ↓
📡 Parámetros en vivo + mediciones
         ↓
🧹 Validación de los datos
         ↓
🔍 Relación entre síntomas, códigos y valores
         ↓
🧪 Pruebas específicas
         ↓
✅ Causa probable respaldada por evidencia
         ↓
🛠️ Decisión técnica
```

---

## 10. 🏁 Conclusiones

- El diagnóstico electrónico automotriz puede formularse como un problema de ciencia de datos porque integra múltiples fuentes y requiere transformar evidencia en una decisión técnica.

- El inventario construido supera el mínimo solicitado y contiene datos estructurados, semiestructurados y no estructurados; esta variedad obliga a definir reglas claras de organización y calidad.

- La analítica diagnóstica es el enfoque principal porque la pregunta central busca explicar por qué ocurre una falla. Las analíticas predictiva y prescriptiva serían etapas futuras si se dispone de suficiente historial.

- El caso de un taller individual no se considera necesariamente Big Data; sin embargo, presenta variedad, veracidad y valor significativos y podría escalar a Big Data con telemetría de grandes flotas.

- El ciclo pregunta → obtener → limpiar → analizar → visualizar → decidir permite documentar el proceso de forma ordenada y evita que la decisión dependa exclusivamente de una lectura aislada.

---

## 11. 📚 Referencias en formato IEEE

[1] U.S. Environmental Protection Agency (EPA), "OBDII Test Procedures," documento de procedimientos de diagnóstico a bordo.  
<https://www.epa.gov/sites/default/files/2018-02/documents/table_e_ut_section_x_vehicle_inspection_and_maintenance_program.pdf>

[2] IBM, "Structured vs. Unstructured Data: What's the Difference?", IBM Think.  
<https://www.ibm.com/think/topics/structured-vs-unstructured-data>

[3] IBM, "What Is Diagnostic Analytics?", IBM Think.  
<https://www.ibm.com/think/topics/diagnostic-analytics>

[4] IBM, "What is Big Data?", IBM Think.  
<https://www.ibm.com/think/topics/big-data>

[5] U.S. Environmental Protection Agency (EPA), "On-Board Diagnostic (OBD) Regulations and Requirements: Questions and Answers."  
<https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P100LW9G.TXT>

---

🚗 **Ciencia de Datos aplicada al diagnóstico automotriz** 🔍  
CORHUILA · Facultad de Ingeniería · 2026-B
