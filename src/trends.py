"""Helpers for skill-trend analysis and polynomial regression."""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

LANG_COLS = ["LanguageHaveWorkedWith", "LanguageWorkedWith"]


def find_col(df, candidates):
    """Return the first column name from `candidates` that exists."""
    for name in candidates:
        if name in df.columns:
            return name
    return None


def skill_shares(df, col):
    """% of people who answered `col` that use each item (a Series)."""
    answered = df[col].dropna()
    items = answered.str.split(";").explode().str.strip()
    return items.value_counts() / len(answered) * 100


def share_table(data, candidates=LANG_COLS, top_n=12):
    """Table: rows = items (e.g. languages), columns = years, values = % users.
    Keeps the top_n items of the latest year."""
    per_year = {}
    for year, df in data.items():
        col = find_col(df, candidates)
        if col is None:
            print(year, "-> column not found, skipped")
            continue
        per_year[year] = skill_shares(df, col)
    table = pd.DataFrame(per_year).sort_index(axis=1)
    latest = table.columns.max()
    top = table[latest].sort_values(ascending=False).head(top_n).index
    return table.loc[top].round(2)


def poly_model(degree):
    """Polynomial regression = make polynomial features + linear regression."""
    return make_pipeline(PolynomialFeatures(degree), LinearRegression())


def loo_mse(x, y, degree):
    """Leave-one-out error: hide each point once, predict it, average the error."""
    scores = cross_val_score(poly_model(degree), x, y, cv=LeaveOneOut(),
                             scoring="neg_mean_squared_error")
    return -scores.mean()