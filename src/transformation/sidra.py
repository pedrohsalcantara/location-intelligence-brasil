from __future__ import annotations

import re
from typing import Any

import pandas as pd


SPECIAL_VALUES = {"...", "-", "X", ""}


def sidra_to_dataframe(rows: list[dict[str, Any]]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    if not df.empty and str(df.iloc[0].get("NC", "")).startswith("Nível Territorial"):
        df = df.iloc[1:].reset_index(drop=True)
    df.columns = [clean_column_name(col) for col in df.columns]
    return df


def clean_column_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^0-9a-zA-ZÀ-ÿ]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value


def parse_sidra_value(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if text in SPECIAL_VALUES:
        return None
    text = text.replace(".", "").replace(",", ".") if "," in text else text
    try:
        return float(text)
    except ValueError:
        return None


def normalize_sidra_long(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    rename_map = {
        "d1c": "municipality_code",
        "d1n": "municipality_name",
        "d2c": "variable_code",
        "d2n": "variable_name",
        "d3c": "period",
        "v": "value_raw",
    }
    if set(rename_map).issubset(df.columns):
        out = df[list(rename_map)].rename(columns=rename_map).copy()
        out["source"] = source_name
        out["municipality_code"] = out["municipality_code"].astype(str)
        out["period"] = out["period"].astype(str)
        out["variable_code"] = out["variable_code"].astype(str)
        out["value"] = out["value_raw"].map(parse_sidra_value)
        return out

    required = ["município_código", "município", "ano_código", "variável_código", "variável", "valor"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing expected SIDRA columns: {missing}")

    out = df[required].copy()
    out.columns = [
        "municipality_code",
        "municipality_name",
        "period",
        "variable_code",
        "variable_name",
        "value_raw",
    ]
    out["source"] = source_name
    out["municipality_code"] = out["municipality_code"].astype(str)
    out["period"] = out["period"].astype(str)
    out["variable_code"] = out["variable_code"].astype(str)
    out["value"] = out["value_raw"].map(parse_sidra_value)
    return out


def pivot_indicators(df: pd.DataFrame, indicator_map: dict[str, str]) -> pd.DataFrame:
    mapped = df[df["variable_code"].isin(indicator_map)].copy()
    mapped["indicator"] = mapped["variable_code"].map(indicator_map)
    wide = (
        mapped.pivot_table(
            index=["municipality_code", "municipality_name", "period"],
            columns="indicator",
            values="value",
            aggfunc="first",
        )
        .reset_index()
        .rename_axis(None, axis=1)
    )
    return wide
