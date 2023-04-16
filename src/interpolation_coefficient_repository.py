"""空力係数補間係数リポジトリクラスモジュール."""
from pandas import DataFrame


class InterpolationCoefficientRepository:
    """空力係数補間係数リポジトリクラス."""

    def __init__(self, file_name: str) -> None:
        """コンストラクタ.

        Args:
            file_name (str): 出力ファイル名
        """
        self.__text_io = open(file_name, "w", newline="")

    def __del__(self) -> None:
        """デストラクタ."""
        self.__text_io.close()

    def set_foil_name(self, root_foil_name: str, tips_foil_name: str) -> None:
        """翼型名セットメソッド.

        Args:
            root_foil_name (str): 翼根翼型名
            tips_foil_name (str): 翼端翼型名
        """
        self.__text_io.write(f"Root Foil,{root_foil_name},Tips Foil,{tips_foil_name}\n")
        self.__text_io.write(",CL,,,,,,,,,,,,,,,CD,,,,,,,,,,,,,,,Cm,,,,,,,,,,,,,,,CL/CD\n")
        self.__text_io.write(
            ",1,a,a^2,a^3,a^4,a^5,a^6,ReCL,ReCL^2,ReCL^3,ReCL^4,ReCL^5,1/logReCL,sqrt|a|,a/ReCL"
            ",1,a,a^2,a^3,a^4,a^5,a^6,ReCL,ReCL^2,ReCL^3,ReCL^4,ReCL^5,1/logReCL,sqrt|a|,a/ReCL"
            ",1,a,a^2,a^3,a^4,a^5,a^6,ReCL,ReCL^2,ReCL^3,ReCL^4,ReCL^5,1/logReCL,sqrt|a|,a/ReCL"
            ",1,a,a^2,a^3,a^4,a^5,a^6,ReCL,ReCL^2,ReCL^3,ReCL^4,ReCL^5,1/logReCL,sqrt|a|,a/ReCL\n"
        )

    def set_aerodynamic_coefficient(self, ratio: float, df_coefficient: DataFrame) -> None:
        """空力係数補間係数セットメソッド.

        Args:
            ratio (float): 翼型混合率
            df_coefficient (DataFrame): 空力係数補間係数
        """
        self.__text_io.write(f"{100*ratio},")
        df_coefficient.loc[["CL"], :].to_csv(self.__text_io, header=False, index=False, mode="a", lineterminator=",")
        df_coefficient.loc[["CD"], :].to_csv(self.__text_io, header=False, index=False, mode="a", lineterminator=",")
        df_coefficient.loc[["CM"], :].to_csv(self.__text_io, header=False, index=False, mode="a", lineterminator=",")
        df_coefficient.loc[["CL/CD"], :].to_csv(self.__text_io, header=False, index=False, mode="a")
