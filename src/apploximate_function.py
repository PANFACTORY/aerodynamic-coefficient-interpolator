"""空力係数近似関数モジュール."""
import numpy as np
from pandas import DataFrame


def fit_alpha_re_15(df: DataFrame) -> DataFrame:
    """空力係数近似関数.

    f(x)=a0 + a1a + a2a^2 + a3a^3 + a4a^4 + a5a^5 + a6a^6 + a7Re + a8Re^2
         + a9Re^3 + a10Re^4 + a11Re^5 + a12(1/lnRe) + a13sqrt|a| + a14(a/Re)

    Args:
        df (DataFrame): 空力係数のデータフレーム

    Returns:
        DataFrame: 空力係数近似関数の係数のデータフレーム
    """
    df_base = df[["alpha"]].copy()
    df_base.insert(loc=0, column="const", value=1.0)
    df_base["alpha^2"] = pow(df_base["alpha"], 2)
    df_base["alpha^3"] = pow(df_base["alpha"], 3)
    df_base["alpha^4"] = pow(df_base["alpha"], 4)
    df_base["alpha^5"] = pow(df_base["alpha"], 5)
    df_base["alpha^6"] = pow(df_base["alpha"], 6)
    df_base["Re"] = df["Re"].copy()
    df_base["Re^2"] = pow(df_base["Re"], 2)
    df_base["Re^3"] = pow(df_base["Re"], 3)
    df_base["Re^4"] = pow(df_base["Re"], 4)
    df_base["Re^5"] = pow(df_base["Re"], 5)
    df_base["1/log10(Re)"] = 1 / np.log10(df_base["Re"])
    df_base["sqrt(abs(alpha))"] = np.sqrt(np.abs(df_base["alpha"]))
    df_base["alpha/Re"] = df_base["alpha"] / df_base["Re"]

    df_measurement = df[["CL", "CD", "CM"]].copy()
    df_measurement["CL/CD"] = df["CL"] / df["CD"]

    df_result = df_measurement.T.dot(df_base.dot(np.linalg.inv(df_base.T.dot(df_base))))
    df_result.columns = df_base.columns
    return df_result
