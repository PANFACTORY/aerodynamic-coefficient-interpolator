"""エントリポイント."""
import os

import click
from dotenv import load_dotenv

from src.apploximate_function import fit_alpha_re_15
from src.xfoil_wrapper import XFoilWrapper

load_dotenv()

VERSION = "1.0.0"

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

        xfoil = XFoilWrapper(os.getenv("XFOIL_PATH", DEFAULT_XFOIL_PATH))
        partition = int(os.getenv("PARTITION", DEFAULT_PARTITION))
        alpha_min = float(os.getenv("ALPHA_MIN", DEFAULT_ALPHA_MIN))
        alpha_max = float(os.getenv("ALPHA_MAX", DEFAULT_ALPHA_MAX))
        alpha_step = float(os.getenv("ALPHA_STEP", DEFAULT_ALPHA_STEP))
        re_min = float(os.getenv("RE_MIN", DEFAULT_RE_MIN))
        re_max = float(os.getenv("RE_MAX", DEFAULT_RE_MAX))
        re_step = float(os.getenv("RE_STEP", DEFAULT_RE_STEP))

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

            with click.progressbar(range(partition + 1)) as bar:
                for i in bar:
                    df_foil = xfoil.mix(df_foil_root, df_foil_tips, i / float(partition))
                    df_analysis = xfoil.analyze(df_foil, alpha_min, alpha_max, alpha_step, re_min, re_max, re_step)
                    df_coefficient = fit_alpha_re_15(df_analysis)
                    f.write(f"{100*i/float(partition)},")
                    df_coefficient.loc[["CL"], :].to_csv(f, header=False, index=False, mode="a", lineterminator=",")
                    df_coefficient.loc[["CD"], :].to_csv(f, header=False, index=False, mode="a", lineterminator=",")
                    df_coefficient.loc[["CM"], :].to_csv(f, header=False, index=False, mode="a", lineterminator=",")
                    df_coefficient.loc[["CL/CD"], :].to_csv(f, header=False, index=False, mode="a")

        click.echo(click.style("Successfully.", fg="green"))
    except Exception as e:
        click.echo(click.style(f"Error. :{e}", fg="red"))
    finally:
        click.echo("-----------Program end-----------")


main(prog_name="interpolator")
