"""空力係数近似関数モジュール."""
import numpy as np
from pandas import DataFrame


class AlphaRe15:
    """空力係数近似関数クラス.

    f(x)=a0 + a1a + a2a^2 + a3a^3 + a4a^4 + a5a^5 + a6a^6 + a7Re + a8Re^2
            + a9Re^3 + a10Re^4 + a11Re^5 + a12(1/lnRe) + a13sqrt|a| + a14(a/Re)
    """

    def __init__(self, df: DataFrame) -> None:
        """コンストラクタ.

        Args:
            df (DataFrame): 空力係数のデータフレーム
        """
        df_base = AlphaRe15.__get_base_function_value(df)
        df_measurement = df[["CL", "CD", "CM"]].copy()
        df_measurement["CL/CD"] = df["CL"] / df["CD"]
        self.df_coefficient = df_measurement.T.dot(df_base.dot(np.linalg.inv(df_base.T.dot(df_base))))
        self.df_coefficient.columns = df_base.columns

    def predict(self, df: DataFrame) -> DataFrame:
        """空力係数近似値計算メソッド.

        Args:
            df (DataFrame): 迎角、レイノルズ数のDataFrame

        Returns:
            DataFrame: 空力係数近似値のDataFrame
        """
        return AlphaRe15.__get_base_function_value(df).dot(self.df_coefficient.T)

    @staticmethod
    def __get_base_function_value(df: DataFrame) -> DataFrame:
        """基底関数取得メソッド.

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
        df_base["1/log10(Re)"] = 1 / np.log(df_base["Re"])
        df_base["sqrt(abs(alpha))"] = np.sqrt(np.abs(df_base["alpha"]))
        df_base["alpha/Re"] = df_base["alpha"] / df_base["Re"]
        return df_base
