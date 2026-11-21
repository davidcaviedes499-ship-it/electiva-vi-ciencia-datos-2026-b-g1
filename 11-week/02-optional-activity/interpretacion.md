# Semana 11 · Interpretación de la serie

**Estudiante:** Juan David Caviedes Cortes · **Usuario GitHub:** davidcaviedes499-ship-it

La serie son las ventas diarias simuladas de una tienda durante 2024 y 2025, agregadas por mes con `resample` y suavizadas con una media móvil de 3 meses.

**Tendencia:** las ventas suben de forma sostenida, unas 165 unidades más cada mes, y el total de 2025 fue 15,4% mayor que el de 2024.

**Estacionalidad:** cada año hay un pico en diciembre (489 unidades diarias en promedio) y una caída a mitad de año (junio, 279). Además, se vende más los sábados y domingos (422 unidades) que entre semana (353).

Como la serie la simulé yo con esos patrones, el análisis los recupera bien; con ventas reales se verían menos limpios.
