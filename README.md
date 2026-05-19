# EDA_Steam_F2P_vs_Paid

**Análisis Exploratorio de Datos: ¿en qué se diferencian los juegos Free-to-Play (F2P) de los juegos de pago en Steam?**

Proyecto EDA del bootcamp de Data Science. Estudio del catálogo completo de Steam (~122.000 juegos) para entender, a partir del dato, las diferencias reales de comportamiento, recepción y volumen entre los dos grandes modelos de negocio que conviven en la plataforma.

---

## Descripción del proyecto

Steam es la mayor plataforma de distribución de videojuegos para PC del mundo. En ella conviven dos modelos de negocio muy distintos:

- **Juegos de pago** — modelo clásico: el usuario paga una vez por el producto.
- **Juegos Free-to-Play (F2P)** — el juego es gratuito y monetiza vía microtransacciones, cosméticos, pases de batalla, suscripciones, etc.

Este análisis busca responder con datos cómo se comportan ambos modelos en términos de **recepción crítica** (% de reseñas positivas), **catálogo por géneros**, **volumen de usuarios concurrentes** y **evolución temporal** dentro del catálogo de Steam.

## Hipótesis planteadas

1. **H1 — Recepción:** Entre juegos con ≥50 reseñas totales, los F2P obtienen un porcentaje medio de reseñas positivas significativamente menor que los juegos de pago.
2. **H2 — Géneros:** La distribución de géneros entre F2P y de pago es significativamente distinta. Los F2P se concentran en MMO, MOBA, Battle Royale y casual; los de pago se reparten más en RPG, aventura, simulación y estrategia.
3. **H3 — Volumen de usuarios:** Los juegos F2P tienen una mediana de pico de jugadores concurrentes (Peak CCU) muy superior a los de pago, aunque su recepción sea peor.
4. **H4 — Tendencia temporal:** La proporción de lanzamientos F2P sobre el total ha crecido año a año desde 2010, reflejando un cambio de modelo de la industria.

## Tecnologías utilizadas

- **Python 3.10+**
- **pandas** — manipulación de datos
- **numpy** — operaciones numéricas
- **matplotlib / seaborn** — visualización
- **scipy.stats** — tests estadísticos (chi-cuadrado, Mann-Whitney U)
- **Jupyter Notebook** — desarrollo del análisis

## Estructura del repositorio

```
EDA_Steam_F2P_vs_Paid/
├── README.md              ← este archivo
├── main.ipynb             ← notebook final consolidado del EDA
├── Memoria.pdf            ← memoria técnica (10-15 páginas)
├── Presentacion.pdf       ← diapositivas de la presentación ejecutiva
├── .gitignore
└── src/
    ├── data/              ← dataset (raw NO subido; ver "Reproducción")
    ├── img/               ← figuras y visualizaciones exportadas
    ├── notebooks/         ← notebooks de desarrollo por fases
    └── utils/             ← funciones auxiliares reutilizables
```

## Reproducción

### 1. Descargar el dataset

El archivo `games.csv` (~372 MB, >100 MB) NO está incluido en el repositorio por exceder el límite de GitHub. Para reproducir el análisis:

1. Descargar **Steam Games Dataset** de FronkonGames desde una de estas fuentes:
   - HuggingFace (sin login): https://huggingface.co/datasets/FronkonGames/steam-games-dataset
   - Kaggle: https://www.kaggle.com/datasets/fronkongames/steam-games-dataset
2. Colocar el archivo `games.csv` en `src/data/games.csv`.

### 2. Instalar dependencias

```bash
pip install pandas numpy matplotlib seaborn scipy jupyter pyarrow
```

> Nota: `pyarrow` se usa para leer/escribir el `games_clean_sample.parquet` (versión limpia y comprimida del dataset, ~8 MB, que sí está incluida en el repo para reproducibilidad rápida).

### 3. Ejecutar el notebook

```bash
jupyter notebook main.ipynb
```

Ejecutar todas las celdas en orden. El notebook genera todas las visualizaciones del análisis y las exporta a `src/img/`.

## Principales conclusiones

Tras filtrar el catálogo a los 58.251 juegos con tracción (≥10 reseñas o Peak CCU > 0), los resultados de las cuatro hipótesis son:

| Hipótesis | Veredicto | Evidencia |
|-----------|-----------|-----------|
| **H1** — F2P obtienen menor % de reseñas positivas (≥50 reviews) | ✅ Confirmada | Mediana F2P 79,2 % vs Pago 82,4 %. Mann–Whitney p ≈ 10⁻³² |
| **H2** — La distribución de géneros entre F2P y Pago es distinta | ✅ Confirmada | χ² = 4.135, p ≈ 0 |
| **H3** — F2P > Pago en Peak CCU mediano | ❌ Refutada (con matiz) | Mediana = 0 en ambos. Pero 5 de los 10 juegos con más jugadores son F2P |
| **H4** — % de lanzamientos F2P crece desde 2010 | ❌ Refutada (con hallazgo) | No es monotónica: 8,6 % (2010) → 22,4 % (2020) → 7,3 % (2024). Curva en U invertida |

**Tres ideas centrales para llevarse a casa:**

1. **F2P es un juego de extremos:** cinco de los diez juegos más jugados de Steam son F2P, pero la mediana de jugadores concurrentes es cero. Es un modelo "winner-take-all".
2. **La calidad percibida apenas difiere:** F2P y de pago se mueven entre el 79–82 % de reseñas positivas. La creencia de que "F2P = peor juego" es una caricatura.
3. **El mercado se aleja del F2P:** la cuota de lanzamientos F2P se ha desplomado tras la pandemia (del 22 % en 2020 al 7 % en 2024).

## Autor

- **Isaac Frr** — [GitHub](https://github.com/IsaacFrr) · [LinkedIn](#)

## Fuente de datos

Dataset: **Steam Games Dataset** por FronkonGames (actualizado en enero 2026, ~122.000 juegos). Datos extraídos de la Steam Web API + SteamSpy. Licencia: MIT.
