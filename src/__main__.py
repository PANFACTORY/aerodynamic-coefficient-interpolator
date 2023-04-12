"""エントリポイント."""
import os
import sys

from dotenv import load_dotenv

from src.apploximate_function import fit_alpha_re_15
from src.xfoil_wrapper import XFoilWrapper

load_dotenv()

try:
    print("----------Program start----------")

    if len(sys.argv) != 4:
        raise Exception("Commandline argument number is invalid.")
    root_foil_name = sys.argv[1]
    tips_foil_name = sys.argv[2]
    output_file_name = sys.argv[3]

    xfoil = XFoilWrapper(os.getenv("XFOIL_PATH", "./xfoil.exe"))
    partition = int(os.getenv("PARTITION", "10"))
    alpha_min = float(os.getenv("ALPHA_MIN", "0"))
    alpha_max = float(os.getenv("ALPHA_MAX", "10"))
    alpha_step = float(os.getenv("ALPHA_STEP", "0.1"))
    re_min = float(os.getenv("RE_MIN", "200000"))
    re_max = float(os.getenv("RE_MAX", "700000"))
    re_step = float(os.getenv("RE_STEP", "50000"))

    df_foil_root = XFoilWrapper.load_foil(root_foil_name)
    df_foil_tips = XFoilWrapper.load_foil(tips_foil_name)

    with open(output_file_name, "w", newline="") as f:
        f.write(f"Root Foil,{root_foil_name},Tips Foil,{tips_foil_name}\n")
        f.write(",CL,,,,,,,,,,,,,,,CD,,,,,,,,,,,,,,,Cm,,,,,,,,,,,,,,,CL/CD\n")
        f.write(
            ",1,a,a^2,a^3,a^4,a^5,a^6,ReCL,ReCL^2,ReCL^3,ReCL^4,ReCL^5,1/logReCL,sqrt|a|,a/ReCL"
            ",1,a,a^2,a^3,a^4,a^5,a^6,ReCL,ReCL^2,ReCL^3,ReCL^4,ReCL^5,1/logReCL,sqrt|a|,a/ReCL"
            ",1,a,a^2,a^3,a^4,a^5,a^6,ReCL,ReCL^2,ReCL^3,ReCL^4,ReCL^5,1/logReCL,sqrt|a|,a/ReCL"
            ",1,a,a^2,a^3,a^4,a^5,a^6,ReCL,ReCL^2,ReCL^3,ReCL^4,ReCL^5,1/logReCL,sqrt|a|,a/ReCL\n"
        )

        for i in range(partition + 1):
            df_foil = xfoil.mix(df_foil_root, df_foil_tips, i / float(partition))
            df_analysis = xfoil.analyze(df_foil, alpha_min, alpha_max, alpha_step, re_min, re_max, re_step)
            df_coefficient = fit_alpha_re_15(df_analysis)
            f.write(f"{100*i/float(partition)},")
            df_coefficient.loc[["CL"], :].to_csv(f, header=False, index=False, mode="a", lineterminator=",")
            df_coefficient.loc[["CD"], :].to_csv(f, header=False, index=False, mode="a", lineterminator=",")
            df_coefficient.loc[["CM"], :].to_csv(f, header=False, index=False, mode="a", lineterminator=",")
            df_coefficient.loc[["CL/CD"], :].to_csv(f, header=False, index=False, mode="a")
            print(f"* {100*i/float(partition)}% finish")
except Exception as e:
    print(e)
finally:
    print("-----------Program end-----------")
