"""
data_loader.py
--------------
Funciones reutilizables para cargar, limpiar y enriquecer el dataset
de Steam Games (FronkonGames, HuggingFace/Kaggle).

Uso tipico desde un notebook:

    from src.utils.data_loader import load_raw, clean_steam, add_features

    df_raw = load_raw()
    df = clean_steam(df_raw)
    df = add_features(df)
"""
from __future__ import annotations

from pathlib import Path
import pandas as pd
import numpy as np


# Ruta por defecto al CSV bruto (relativa a la raiz del repo)
DEFAULT_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "games.csv"

# El CSV de HuggingFace/Kaggle tiene un bug conocido: el header lista
# 'DiscountDLC count' como una sola columna pero los datos contienen
# dos columnas separadas ('Discount' y 'DLC count'). Esto desalinea
# todas las columnas posteriores. Forzamos los nombres correctos al cargar.
COLUMNAS_REALES = [
    "AppID", "Name", "Release date", "Estimated owners", "Peak CCU",
    "Required age", "Price", "Discount", "DLC count", "About the game",
    "Supported languages", "Full audio languages", "Reviews", "Header image",
    "Website", "Support url", "Support email", "Windows", "Mac", "Linux",
    "Metacritic score", "Metacritic url", "User score", "Positive", "Negative",
    "Score rank", "Achievements", "Recommendations", "Notes",
    "Average playtime forever", "Average playtime two weeks",
    "Median playtime forever", "Median playtime two weeks",
    "Developers", "Publishers", "Categories", "Genres", "Tags",
    "Screenshots", "Movies",
]

# Columnas que NO aportan al EDA y se eliminan en la limpieza
COLS_DROP = [
    "Movies",
    "Score rank",
    "Metacritic url",
    "Reviews",
    "Notes",
    "Website",
    "Support url",
    "Support email",
    "Header image",
    "About the game",
    "Screenshots",
    "Full audio languages",
]

# Umbral minimo de resenas para considerar que un juego tiene "traccion"
MIN_REVIEWS_TRACCION = 10


def load_raw(path=DEFAULT_DATA_PATH):
    """Carga el CSV bruto con el header reparado."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"No se encuentra {path}. Ver README -> Reproduccion -> Descargar el dataset."
        )
    df = pd.read_csv(
        path,
        header=None,
        skiprows=1,
        names=COLUMNAS_REALES,
        engine="python",
    )
    return df


def clean_steam(df, drop_cols=None, filtrar_traccion=True, min_reviews=MIN_REVIEWS_TRACCION):
    """Limpieza del dataset bruto de Steam."""
    df = df.copy()
    drop = drop_cols if drop_cols is not None else COLS_DROP
    df.drop(columns=[c for c in drop if c in df.columns], inplace=True)

    df["Release date"] = pd.to_datetime(
        df["Release date"], errors="coerce", format="mixed"
    )

    num_cols = [
        "Price", "Discount", "DLC count", "Peak CCU", "Positive", "Negative",
        "Metacritic score", "User score", "Recommendations",
        "Average playtime forever", "Median playtime forever",
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    for c in ["Windows", "Mac", "Linux"]:
        if c in df.columns:
            df[c] = df[c].astype(bool)

    if "AppID" in df.columns:
        df.drop_duplicates(subset=["AppID"], keep="first", inplace=True)

    if filtrar_traccion:
        total_reviews = df["Positive"].fillna(0) + df["Negative"].fillna(0)
        peak_ccu = df["Peak CCU"].fillna(0)
        mask_reviews = total_reviews >= min_reviews
        mask_ccu = peak_ccu > 0
        mask = mask_reviews | mask_ccu
        df = df.loc[mask].copy()

    df.reset_index(drop=True, inplace=True)
    return df


def add_features(df):
    """Crea variables derivadas utiles para el analisis."""
    df = df.copy()
    df["modelo_negocio"] = np.where(df["Price"].fillna(0) == 0, "F2P", "Pago")
    df["total_reviews"] = df["Positive"].fillna(0) + df["Negative"].fillna(0)
    df["pct_positivas"] = np.where(
        df["total_reviews"] > 0,
        df["Positive"] / df["total_reviews"] * 100,
        np.nan,
    )
    df["anyo_lanzamiento"] = df["Release date"].dt.year
    df["decada"] = (df["anyo_lanzamiento"] // 10 * 10).astype("Int64")
    if "Genres" in df.columns:
        df["genero_principal"] = (
            df["Genres"].fillna("Sin genero").astype(str).str.split(",").str[0].str.strip()
        )
    df["n_plataformas"] = df[["Windows", "Mac", "Linux"]].sum(axis=1).astype(int)
    return df


def resumen_calidad(df):
    """Genera un resumen rapido de calidad (dtype, nulos, unicos, ejemplo)."""
    return pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "nulos": df.isnull().sum(),
        "pct_nulos": (df.isnull().mean() * 100).round(2),
        "unicos": df.nunique(),
        "ejemplo": [
            df[c].dropna().iloc[0] if df[c].notna().any() else None
            for c in df.columns
        ],
    })
