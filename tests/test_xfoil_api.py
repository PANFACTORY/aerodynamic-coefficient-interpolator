from pandas import DataFrame

from src.apploximate_function import AlphaRe15
from src.xfoil_api import XFoilApi


def test_xfoil_api() -> None:
    df_foil = XFoilApi.load_foil("./tests/DAE21.dat")
    api = XFoilApi("./xfoil.exe")

    df_analysis = api.analyze(df_foil, 0.0, 10.0, 1.0, 200000.0, 700000.0, 50000.0)
    model = AlphaRe15(df_analysis)

    re = 530000.0
    df_analysis_check = api.analyze(df_foil, 0.0, 10.0, 1.0, re, re, 1.0)
    df_base = DataFrame(data=[[a, re] for a in range(0, 11, 1)], columns=["alpha", "Re"])

    print(df_analysis_check)
    print(model.predict(df_base))
