"""エントリポイント."""
import os
import sys

from dotenv import load_dotenv

from .xfoil_wrapper import XFoilWrapper

load_dotenv()

try:
    print("----------Program start----------")
    if len(sys.argv) != 2:
        raise Exception("Commandline argument number is invalid.")

    xfoil = XFoilWrapper(os.getenv("XFOIL_PATH", "./xfoil.exe"))
    df_foil = XFoilWrapper.load_foil(sys.argv[1])
    result = xfoil.analyze(df_foil, 5, 10, 0.5, 500000)
    print(result)
except Exception as e:
    print(e)
finally:
    print("-----------Program end-----------")
