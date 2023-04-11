"""エントリポイント."""
import os
import sys

from dotenv import load_dotenv

from .apploximate_function import fit_alpha_re_15
from .xfoil_wrapper import XFoilWrapper

load_dotenv()

try:
    print("----------Program start----------")

    if len(sys.argv) != 4:
        raise Exception("Commandline argument number is invalid.")

    xfoil = XFoilWrapper(os.getenv("XFOIL_PATH", "./xfoil.exe"))

    df_foil_root = XFoilWrapper.load_foil(sys.argv[1])
    df_foil_tips = XFoilWrapper.load_foil(sys.argv[2])

    with open(sys.argv[3], "w") as f:
        f.write(f"Root Foil,{sys.argv[1]},Tips Foil,{sys.argv[2]}\n")
        f.write(",CL,,,,,,,,,,,,,,,CD,,,,,,,,,,,,,,,Cm,,,,,,,,,,,,,,,CL/CD\n")
        f.write(
            ",1,a,a^2,a^3,a^4,a^5,a^6,ReCL,ReCL^2,ReCL^3,ReCL^4,ReCL^5,1/logReCL,√|a|,a/ReCL"
            ",1,a,a^2,a^3,a^4,a^5,a^6,ReCL,ReCL^2,ReCL^3,ReCL^4,ReCL^5,1/logReCL,√|a|,a/ReCL"
            ",1,a,a^2,a^3,a^4,a^5,a^6,ReCL,ReCL^2,ReCL^3,ReCL^4,ReCL^5,1/logReCL,√|a|,a/ReCL"
            ",1,a,a^2,a^3,a^4,a^5,a^6,ReCL,ReCL^2,ReCL^3,ReCL^4,ReCL^5,1/logReCL,√|a|,a/ReCL\n"
        )

        # 各翼型混合率について
        for i in range(11):
            # 各迎角、Reynolds数について空力係数を計算
            df_foil = xfoil.mix(df_foil_root, df_foil_tips, i / 10.0)
            df_analysis = xfoil.analyze(df_foil, 5.0, 10.0, 0.5, 200000.0, 300000.0, 100000.0)

            # 近似式の係数を算出
            df_coefficient = fit_alpha_re_15(df_analysis)
            print(df_coefficient)

except Exception as e:
    print(e)
finally:
    print("-----------Program end-----------")
