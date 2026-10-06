# PoC 03: recuperación de fragmentos para RAG

Parte del proyecto de tesis "Plataforma web para la detección temprana del riesgo de sobreendeudamiento en mujeres emprendedoras" (UPC, Taller de Proyecto I, 2026-20).

## Objetivo único
Verificar que, dado un factor de riesgo entregado por SHAP, la búsqueda por similitud recupera fragmentos pertinentes de un corpus de educación financiera.

No valida la redacción del modelo de lenguaje (eso le corresponde a la PoC 04), ni la calidad del corpus definitivo, ni la utilidad del consejo.

## Datos
- **Corpus:** sustituto de 16 fragmentos en español: 12 de educación financiera y 4 distractores (seguros, pensiones, fondos mutuos, tipo de cambio). Se usó un sustituto porque la SBS bloqueó la descarga automatizada de sus guías.
- **Variables:** las 8 consultas corresponden a variables del diseño de septiembre de 2026.
- **Verdad de referencia:** los fragmentos pertinentes de cada variable se definieron a mano antes de correr (`RELEVANTES` en `corpus.py`).

## Método
- Modelo de embeddings `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, de 384 dimensiones.
- Similitud coseno, con los 4 fragmentos más cercanos por consulta (top-4).
- Se comparan dos formas de construir la consulta: el nombre crudo de la variable o una frase en lenguaje financiero tomada de una tabla de mapeo.

## Cómo correrla
```
pip install -r requirements.txt
python poc_rag.py
```
La primera vez descarga el modelo de embeddings, de unos 470 MB.

## Resultado
| Configuración | P@4 | R@4 | MRR | Distractores recuperados |
|---|---|---|---|---|
| Con tabla de mapeo | 0.438 | 0.938 | 0.833 | 2 / 32 |
| Sin mapeo (nombre de la variable) | 0.281 | 0.583 | 0.5 | 2 / 32 |

- **Techo teórico de P@4 con este corpus:** 0.469. Varias variables tienen menos de 4 fragmentos pertinentes, así que la precisión nunca puede llegar a 1.
- **Similitud de los distractores recuperados:** 0.474 a 0.498.
- **Similitud de los fragmentos pertinentes recuperados:** 0.513 a 0.845.
- **Primer resultado equivocado:** en `ratio_cuota_ingreso` y en `ingreso_peor_mes`.

## Umbral de corte de 0.55
Con un umbral de 0.55 se descartan los 2 distractores y se conservan 13 de los 14 fragmentos pertinentes recuperados.

El único pertinente que queda por debajo es F09 (similitud 0.513), en la consulta de `ratio_cuota_ingreso`. Por eso los pertinentes no quedan todos por encima de 0.60: el rango real es el que muestra esta corrida.

## Decisión de diseño
- Se adopta la tabla de mapeo de variable a consulta en lenguaje financiero, porque eleva R@4 de 0.583 a 0.938.
- Se adopta el umbral de 0.55 para descartar fragmentos sin respaldo.

## Archivos
- `poc_rag.py`: script.
- `corpus.py`: corpus, tabla de mapeo y verdad de referencia.
- `resultado_poc_rag.json`: salida estructurada.
- `salida_consola.txt`: salida completa de la consola.

## Corrida de referencia
6 de octubre de 2026, Linux, Python 3.12.3. Las métricas son idénticas a la corrida original del 20 de septiembre de 2026. Los tiempos de carga e indexación dependen de la máquina, así que no son mediciones controladas de rendimiento.
