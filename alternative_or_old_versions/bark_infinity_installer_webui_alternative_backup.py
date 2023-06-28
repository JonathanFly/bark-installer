import argparse
import glob
import os
import shutil
import site
import subprocess
import sys
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)

# Constants
SCRIPT_DIR = Path.cwd()
CONDA_ENV_PATH = SCRIPT_DIR / "installer_files" / "env"
CONDA_ENV_YML_FILE = "environment-cuda-installer_alternative.yml"
BARK_DIR = SCRIPT_DIR / "bark"


def build_conda_path():
    if sys.platform.startswith("win"):
        return SCRIPT_DIR / "installer_files" / "conda" / "condabin" / "conda.bat"
    else:
        return (
            SCRIPT_DIR / "installer_files" / "conda" / "etc" / "profile.d" / "conda.sh"
        )


def run_conda_cmd(cmd, assert_success=False, capture_output=False, env=None):
    conda_path = build_conda_path()
    cmd = (
        f'"{conda_path}" activate "{CONDA_ENV_PATH}" >nul && ' + cmd
        if sys.platform.startswith("win")
        else f'. "{conda_path}" && conda activate "{CONDA_ENV_PATH}" && {cmd}'
    )
    return run_cmd(cmd, assert_success, capture_output, env)


def run_cmd(cmd, assert_success=False, capture_output=False, env=None):
    result = subprocess.run(cmd, shell=True, capture_output=capture_output, env=env)
    if assert_success and result.returncode != 0:
        logging.error(
            f"Command '{cmd}' failed with exit status code '{result.returncode}'. Exiting..."
        )
        sys.exit()
    return result


def check_env():
    # If we have access to conda, we are probably in an environment
    conda_exist = run_cmd("conda", capture_output=True).returncode == 0
    if not conda_exist:
        print("Conda is not installed. Exiting...")
        sys.exit()

    # Ensure this is a new environment and not the base environment
    if os.environ["CONDA_DEFAULT_ENV"] == "base":
        print("Create an environment for this project and activate it. Exiting...")
        sys.exit()


def install_dependencies():
    commands = [
        ("conda install -n base -y conda-libmamba-solver", True),
        (f"conda env update  --file {CONDA_ENV_YML_FILE} --solver=libmamba", True),
        ("pip install -r requirements-extra.txt", False),
        ("conda update -y --all --solver=libmamba", True),
    ]

    if BARK_DIR.exists():
        logging.info(f"Running in directory: {SCRIPT_DIR}")
    else:
        commands.extend(
            [
                ("conda update -y -n base conda", True),
                ("conda install -n base -y conda-libmamba-solver", True),
                ("conda install -y -k pip --solver=libmamba", True),
                ("pip install --no-input ffmpeg-downloader", True),
                ("ffdl install -U --add-path 6.0@full", True),
                ("conda install -y -k git --solver=libmamba", True),
                ("git clone https://github.com/JonathanFly/bark.git", True),
                (
                    f"conda env update --file {CONDA_ENV_YML_FILE} --solver=libmamba",
                    True,
                ),
                (f"conda update -y --all --solver=libmamba", True),
                ("ffdl install -y -U --add-path 6.0@full", False),
                ("pip install -r requirements-extra.txt", False),
            ]
        )

    for cmd, assert_success in commands:
        run_conda_cmd(cmd, assert_success=assert_success)

    print(
        f'\n\nAfter the install finishes, close this window.\n\nClose any text terminals open.\n\nThen click on start_bark_infinity.bat in a fresh explorer window. This seems to be necessary for FFMPEG to be detected after installation. Then click on "LAUNCH_already_installed_bark_infinity_windows"\n\n'
    )

    print(
        f"\nIf you have trouble you can try TROUBLESHOOT_bark_setup_manually_by_entering_the_conda_environment.bat\n\n"
    )

    print(
        f"\nIf you use this terminal you will have to type 'conda deactivate' first. \"\n\n"
    )

    run_cmd(
        f"conda deactivate",
        assert_success=False,
    )

    return


def launch_webui():
    os.chdir("bark")

    run_conda_cmd("git fetch", assert_success=True)
    run_conda_cmd("git checkout installer_test", assert_success=True)
    run_conda_cmd("git pull", assert_success=True)

    # run_cmd(f"python bark_webui.py {CMD_FLAGS}")
    run_cmd(f"python bark_webui.py")


if __name__ == "__main__":
    # Verifies we are in a conda environment
    check_env()

    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Update the web UI.")
    args = parser.parse_args()

    if args.update:
        pass
        # update_dependencies()
    else:
        # If webui has already been installed, skip and run
        if not os.path.exists("bark/") or True:
            install_dependencies()
            os.chdir(SCRIPT_DIR)
