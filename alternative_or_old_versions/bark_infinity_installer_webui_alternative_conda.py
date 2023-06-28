import argparse
import os
import sys
import subprocess
from pathlib import Path
import logging

# Constants
SCRIPT_DIR = Path.cwd()
INSTALLER_FILES_DIR = SCRIPT_DIR / "installer_files"
CONDA_DIR = INSTALLER_FILES_DIR / "conda"
BARK_DIR = SCRIPT_DIR / "bark"
CONDA_ENV_PATH = INSTALLER_FILES_DIR / "env"
CONDA_ENV_YML_FILE = "environment-cuda-installer_alternative.yml"

# Set up logging
logging.basicConfig(level=logging.INFO)

# Dry-run flag
DRY_RUN = False


def get_conda_path():
    conda_path = (
        CONDA_DIR / "condabin" / "conda.bat"
        if sys.platform.startswith("win")
        else CONDA_DIR / "etc" / "profile.d" / "conda.sh"
    )
    return conda_path


def run_cmd(cmd, assert_success=False, capture_output=False, env=None):
    if DRY_RUN:
        print(f"--> {cmd}")
        result = 1
    else:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, env=env)
        if assert_success and result.returncode != 0:
            logging.error(
                f"Command '{cmd}' failed with exit status code '{result.returncode}'. Exiting..."
            )
            sys.exit()

    return result


def run_conda_cmd(cmd, assert_success=False, capture_output=False, env=None):
    conda_path = get_conda_path()
    cmd = (
        f'"{conda_path}" activate "{CONDA_ENV_PATH}" >nul && {cmd}'
        if sys.platform.startswith("win")
        else f'. "{conda_path}" && conda activate "{CONDA_ENV_PATH}" && {cmd}'
    )
    run_cmd(cmd, assert_success, capture_output, env)


def check_env():
    if not DRY_RUN:
        if (
            run_cmd("conda", capture_output=True).returncode != 0
            or os.environ["CONDA_DEFAULT_ENV"] == "base"
        ):
            print(
                "Conda is not installed or you are using base environment. Please install Conda and create a new environment. Exiting..."
            )
            sys.exit()
    else:
        print("--> Dry run start: conda")


def install_dependencies():
    base_commands = [
        ("conda update -y -n base conda", True),
        ("conda install -n base -y conda-libmamba-solver", True),
        (f"conda env update  --file {CONDA_ENV_YML_FILE} --solver=libmamba", True),
        ("pip install -r requirements-extra.txt", False),
        ("conda update -y --all --solver=libmamba", True),
    ]
    bark_commands = [
        ("conda update -y -n base conda", True),
        ("conda install -n base -y conda-libmamba-solver", True),
        ("conda install -y -k pip --solver=libmamba", True),
        ("pip install --no-input ffmpeg-downloader", True),
        ("ffdl install -U --add-path 6.0@full", True),
        ("conda install -y -k git --solver=libmamba", True),
        ("git clone https://github.com/JonathanFly/bark.git", True),
        (f"conda env update --file {CONDA_ENV_YML_FILE} --solver=libmamba", True),
        (f"conda update -y --all --solver=libmamba", True),
        ("ffdl install -y -U --add-path 6.0@full", False),
        ("pip install -r requirements-extra.txt", False),
    ]
    commands = base_commands if BARK_DIR.exists() else bark_commands

    for cmd, assert_success in commands:
        run_conda_cmd(cmd, assert_success=assert_success)

    print(
        f"\n\nClose any open text terminals, and then click on the start_bark_infinity.bat file in a new window. This seems to be necessary for FFMPEG to be detected after installation.\n\nIf you have trouble, you can try TROUBLESHOOT_bark_setup_manually_by_entering_the_conda_environment.bat\n\nRemember, if you use this terminal, you will have to type 'conda deactivate' first."
    )
    run_cmd("conda deactivate", assert_success=False)


def launch_webui():
    os.chdir(BARK_DIR)

    run_conda_cmd("git fetch", assert_success=True)
    run_conda_cmd("git checkout installer_test", assert_success=True)
    run_conda_cmd("git pull", assert_success=True)

    run_cmd("python bark_webui.py")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the commands that would be run, but do not execute them.",
    )
    parser.add_argument("--update", action="store_true", help="Update the web UI.")
    args = parser.parse_args()

    DRY_RUN = args.dry_run

    DRY_RUN = True
    check_env()

    if not args.update and (not BARK_DIR.exists() or True):
        install_dependencies()
        os.chdir(SCRIPT_DIR)
