"""XFoil APIクラスモジュール."""
import os
from subprocess import DEVNULL, PIPE, Popen
from tempfile import TemporaryDirectory

from pandas import DataFrame, concat, read_csv


class XFoilApi:
    """XFoil APIクラス."""

    def __init__(self, xfoil_path: str) -> None:
        """コンストラクタ.

        Args:
            xfoil_path (str): XFoilのパス
        """
        self.__xfoil_path = xfoil_path

    def analyze(
        self, df_foil: DataFrame, amin: float, amax: float, da: float, remin: float, remax: float, dre: float
    ) -> DataFrame:
        """二次元翼解析メソッド.

        Args:
            df_foil (DataFarame): 解析対象の翼根座標データフレーム
            amin (float): 最小迎角
            amax (float): 最大迎角
            da (float): 迎角ステップサイズ
            remin (float): 最小レイノルズ数
            remax (float): 最大レイノルズ数
            dre (float): レイノルズ数ステップサイズ

        Returns:
            DataFrame: 迎角毎の空力係数のデータフレーム
        """
        with TemporaryDirectory() as td:
            XFoilApi.dump_foil(os.path.join(td, "foil.dat"), "", df_foil)

            df_result = DataFrame(data=[], columns=["alpha", "Re", "CL", "CD", "CDp", "CM", "Top_Xtr", "Bot_Xtr"])

            for i in range(int((remax - remin) / dre) + 1):
                re = remin + dre * i

                xfoil = Popen(self.__xfoil_path, stdin=PIPE, stdout=DEVNULL, stderr=DEVNULL, text=True)
                if xfoil.stdin is None:
                    raise Exception("Popen.stdin for XFoil is None.")
                xfoil.stdin.write("plop\n")
                xfoil.stdin.write("gf\n")
                xfoil.stdin.write("\n")
                xfoil.stdin.write(f'load {os.path.join(td, "foil.dat")}\n')
                xfoil.stdin.write("oper\n")
                xfoil.stdin.write("iter 100\n")
                xfoil.stdin.write("Type 3\n")
                xfoil.stdin.write("visc\n")
                xfoil.stdin.write(f"{re}\n")
                xfoil.stdin.write("pacc\n")
                xfoil.stdin.write(f'{os.path.join(td, f"tmp_{i}.out")}\n')
                xfoil.stdin.write("\n")
                xfoil.stdin.write(f"aseq {amin} {amax} {da}\n")
                xfoil.stdin.write("\n")
                xfoil.stdin.write("quit\n")
                xfoil.stdin.close()
                xfoil.wait()

                df_result = concat(
                    [
                        df_result,
                        read_csv(
                            os.path.join(td, f"tmp_{i}.out"),
                            delim_whitespace=True,
                            skiprows=12,
                            header=None,
                            names=["alpha", "CL", "CD", "CDp", "CM", "Top_Xtr", "Bot_Xtr"],
                        ).assign(Re=re),
                    ],
                    ignore_index=True,
                )

            return df_result

    def mix(self, df_foil_root: DataFrame, df_foil_tips: DataFrame, ratio: float) -> DataFrame:
        """翼型混合メソッド.

        Args:
            root_foil_name (DataFrame): 翼根翼型座標データのデータフレーム
            tips_foil_name (DataFrame): 翼端翼型座標データのデータフレーム
            ratio (float): 混合率

        Returns:
            DataFrame: 翼型座標データのデータフレーム
        """
        with TemporaryDirectory() as td:
            XFoilApi.dump_foil(os.path.join(td, "foil_root.dat"), "", df_foil_root)
            XFoilApi.dump_foil(os.path.join(td, "foil_tips.dat"), "", df_foil_tips)

            xfoil = Popen(self.__xfoil_path, stdin=PIPE, stdout=DEVNULL, stderr=DEVNULL, text=True)
            if xfoil.stdin is None:
                raise Exception("Popen.stdin for XFoil is None.")
            xfoil.stdin.write("inte\n")
            xfoil.stdin.write("f\n")
            xfoil.stdin.write(f'{os.path.join(td, "foil_root.dat")}\n')
            xfoil.stdin.write("f\n")
            xfoil.stdin.write(f'{os.path.join(td, "foil_tips.dat")}\n')
            xfoil.stdin.write(f"{ratio}\n")
            xfoil.stdin.write(f"{ratio*100}%\n")  # Foil name in file
            xfoil.stdin.write("PANE\n")
            xfoil.stdin.write(f'SAVE {os.path.join(td, "out.dat")}\n')
            xfoil.stdin.write("quit\n")
            xfoil.stdin.close()
            xfoil.wait()

            return XFoilApi.load_foil(os.path.join(td, "out.dat"))

    @staticmethod
    def load_foil(file_name: str) -> DataFrame:
        """翼型座標ファイルを翼型座標データフレームに変換するメソッド.

        Args:
            file_name (str): 翼型座標ファイル名

        Returns:
            DataFrame: 翼型座標データフレーム
        """
        return read_csv(file_name, delim_whitespace=True, skiprows=1, header=None, names=["x", "y"])

    @staticmethod
    def dump_foil(file_name: str, foil_name: str, df: DataFrame) -> None:
        """翼型座標データフレームを翼型座標ファイルに変換するメソッド.

        Args:
            file_name (str): 翼型座標ファイル名
            foil_name (str): 翼型名（ファイル内に記載）
            df (DataFrame): 翼型座標データフレーム
        """
        with open(file_name, "w") as f:
            f.write(f"{foil_name}\n")
        df.to_csv(file_name, header=False, columns=["x", "y"], index=False, sep=" ", mode="a")
