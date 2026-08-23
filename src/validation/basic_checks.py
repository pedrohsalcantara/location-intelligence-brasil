from __future__ import annotations

import pandas as pd


def summarize_dataframe(df: pd.DataFrame) -> dict[str, object]:
    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "column_names": list(df.columns),
        "null_percent_by_column": {
            col: round(float(df[col].isna().mean() * 100), 2) for col in df.columns
        },
    }


def validate_gold(df: pd.DataFrame) -> list[str]:
    issues: list[str] = []
    if df.empty:
        return ["Gold table is empty."]
    if df["municipality_code"].isna().any():
        issues.append("municipality_code has null values.")
    if df["municipality_code"].duplicated().any():
        issues.append("municipality_code is not unique in Gold.")
    if "population_estimated" in df and (df["population_estimated"].dropna() < 0).any():
        issues.append("population_estimated has negative values.")
    if "gdp_current_brl_thousand" in df and (df["gdp_current_brl_thousand"].dropna() < 0).any():
        issues.append("gdp_current_brl_thousand has negative values.")
    return issues
