"""エントリポイント."""
import os
import traceback

import click
from dotenv import load_dotenv

from src._version import VERSION
from src.approximate_function import AlphaRe15
from src.interpolation_coefficient_repository import InterpolationCoefficientRepository
from src.xfoil_api import XFoilApi

load_dotenv()

DEFAULT_XFOIL_PATH = "./xfoil.exe"
DEFAULT_PARTITION = 10
DEFAULT_ALPHA_MIN = 0
DEFAULT_ALPHA_MAX = 10
DEFAULT_ALPHA_STEP = 0.1
DEFAULT_RE_MIN = 200000
DEFAULT_RE_MAX = 700000
DEFAULT_RE_STEP = 50000


@click.command()
@click.version_option(version=VERSION, message="%(version)s")
@click.argument("root_foil_name", type=str, required=True)
@click.argument("tips_foil_name", type=str, required=True)
@click.argument("output_file_name", type=str, required=True)
def main(root_foil_name: str, tips_foil_name: str, output_file_name: str) -> None:
    """メイン処理.

    Args:
        root_foil_name (str): 翼根翼型ファイル名
        tips_foil_name (str): 翼端翼型ファイル名
        output_file_name (str): 出力ファイル名
    """
    try:
        click.echo("----------Program start----------")

        partition = int(os.getenv("PARTITION", DEFAULT_PARTITION))
        alpha_min = float(os.getenv("ALPHA_MIN", DEFAULT_ALPHA_MIN))
        alpha_max = float(os.getenv("ALPHA_MAX", DEFAULT_ALPHA_MAX))
        alpha_step = float(os.getenv("ALPHA_STEP", DEFAULT_ALPHA_STEP))
        re_min = float(os.getenv("RE_MIN", DEFAULT_RE_MIN))
        re_max = float(os.getenv("RE_MAX", DEFAULT_RE_MAX))
        re_step = float(os.getenv("RE_STEP", DEFAULT_RE_STEP))

        api = XFoilApi(os.getenv("XFOIL_PATH", DEFAULT_XFOIL_PATH))

        df_foil_root = XFoilApi.load_foil(root_foil_name)
        df_foil_tips = XFoilApi.load_foil(tips_foil_name)

        repository = InterpolationCoefficientRepository(output_file_name)
        repository.set_foil_name(root_foil_name, tips_foil_name)

        with click.progressbar(range(partition + 1)) as bar:
            for i in bar:
                ratio = i / float(partition)
                df_foil = api.mix(df_foil_root, df_foil_tips, ratio)
                df_analysis = api.analyze(df_foil, alpha_min, alpha_max, alpha_step, re_min, re_max, re_step)
                model = AlphaRe15(df_analysis)
                repository.set_aerodynamic_coefficient(ratio, model.df_coefficient)

        click.echo(click.style("Successfully.", fg="green"))
    except Exception as e:
        click.echo(click.style(f"{e.__class__.__name__}: {e}", fg="red"))
        click.echo(traceback.format_exc(), err=True)
    finally:
        click.echo("-----------Program end-----------")


main(prog_name="interpolator")
