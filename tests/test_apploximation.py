import math

from src.apploximate_function import AlphaRe15
from src.xfoil_api import XFoilApi


def test_apploximation() -> None:
    df_foil = XFoilApi.load_foil("./tests/DAE21.dat")
    api = XFoilApi("./xfoil.exe")
    df_analysis = api.analyze(df_foil, 0.0, 10.0, 0.5, 200000.0, 700000.0, 50000.0)
    model = AlphaRe15(df_analysis)

    re = 530000.0
    df_analysis_check = api.analyze(df_foil, 0.0, 10.0, 1.0, re, re, 1.0)
    df_predict = model.predict(df_analysis_check[["alpha", "Re"]])
    error = math.sqrt(pow(df_predict["CL"] - df_analysis_check["CL"], 2).sum())
    assert error < 0.05
