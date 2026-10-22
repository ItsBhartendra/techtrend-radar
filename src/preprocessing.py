"""Reusable cleaning and feature-engineering helpers for TechTrend Radar."""

import numpy as np
import pandas as pd


def parse_years(value):
    """Turn answers like 'Less than 1 year' or '12' into numbers."""
    if pd.isna(value):
        return np.nan
    v = str(value).strip()
    if v.startswith("Less than"):
        return 0.5
    if v.startswith("More than"):
        return 51.0
    try:
        return float(v)
    except ValueError:
        return np.nan


def education_level(value):
    """Turn education text into an ordered number (higher = more education)."""
    if pd.isna(value):
        return np.nan
    v = str(value).lower()
    rules = [("primary", 1), ("secondary", 2), ("some college", 3),
             ("associate", 4), ("bachelor", 5), ("master", 6),
             ("professional", 7), ("doctoral", 7)]
    for key, level in rules:
        if key in v:
            return level
    return np.nan


def clean_salary(df, col="ConvertedCompYearly", low_q=0.01, high_q=0.99):
    """Keep rows with a positive salary and remove extreme outliers
    (below the 1st or above the 99th percentile)."""
    out = df[df[col].notna() & (df[col] > 0)].copy()
    lo, hi = out[col].quantile([low_q, high_q])
    out = out[(out[col] >= lo) & (out[col] <= hi)]
    return out, lo, hi


def split_items(series):
    """'Python;SQL;Go' -> ['Python', 'SQL', 'Go'] (empty list if missing)."""
    return series.fillna("").apply(
        lambda x: [i.strip() for i in x.split(";") if i.strip()])


def multi_hot(df, col, top_n, prefix):
    """Make one 0/1 column for each of the top_n most common items."""
    items = split_items(df[col])
    top = items.explode().value_counts().head(top_n).index
    result = {f"{prefix}_{item}": items.apply(lambda lst, it=item: int(it in lst))
              for item in top}
    return pd.DataFrame(result, index=df.index)


def build_features(df, top_countries=10, top_skills=8):
    """Build the feature table X from the cleaned survey DataFrame."""
    X = pd.DataFrame(index=df.index)
    X["years_code"] = df["YearsCode"].apply(parse_years)
    X["edu_level"] = df["EdLevel"].apply(education_level)

    # Skill columns: every column ending in 'HaveWorkedWith'
    tech_cols = [c for c in df.columns if c.endswith("HaveWorkedWith")]
    skill_frames = [multi_hot(df, c, top_skills, c.replace("HaveWorkedWith", ""))
                    for c in tech_cols]
    skills = pd.concat(skill_frames, axis=1)

    # Total number of skills each person listed (all items, not only top ones)
    X["num_skills"] = sum(split_items(df[c]).apply(len) for c in tech_cols)

    # Country: top N countries as 0/1 columns, the rest become 'Other'
    top = df["Country"].value_counts().head(top_countries).index
    country = df["Country"].where(df["Country"].isin(top), "Other")
    country = pd.get_dummies(country, prefix="country").astype(int)

    return pd.concat([X, skills, country], axis=1), tech_cols