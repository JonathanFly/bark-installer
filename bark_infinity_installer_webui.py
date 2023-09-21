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
# CONDA_ENV_YML_FILE = "environment-cuda-installer_alternative.yml"

# Set up logging
logging.basicConfig(level=logging.INFO)


def get_conda_path():
    conda_path = (
        CONDA_DIR / "condabin" / "conda.bat"
        if sys.platform.startswith("win")
        else CONDA_DIR / "etc" / "profile.d" / "conda.sh"
    )
    return conda_path


def run_cmd(cmd, assert_success=False, capture_output=False, env=None, dry_run=False):
    if dry_run:
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


def run_conda_cmd(
    cmd, assert_success=False, capture_output=False, env=None, dry_run=False
):
    conda_path = get_conda_path()
    cmd = (
        f'"{conda_path}" activate "{CONDA_ENV_PATH}" >nul && {cmd}'
        if sys.platform.startswith("win")
        else f'. "{conda_path}" && conda activate "{CONDA_ENV_PATH}" && {cmd}'
    )
    print(f" >>Running command: {cmd}")
    run_cmd(cmd, assert_success, capture_output, env, dry_run)


def check_env(dry_run):
    if not dry_run:
        if (
            run_cmd("conda", capture_output=True, env=None, dry_run=dry_run).returncode != 0  # type: ignore
            or os.environ["CONDA_DEFAULT_ENV"] == "base"
        ):
            print(
                "Conda is not installed or you are using base environment. Please install Conda and create a new environment. Exiting..."
            )
            sys.exit()
    else:
        print("--> Dry run start: conda")


def install_dependencies(dry_run):
    conda_path = get_conda_path()

    base_commands = [
        (f'"{conda_path}"' + " update -y -k -n base conda", True),
        (f'"{conda_path}"' + " install -k -n base -y conda-libmamba-solver", True),
        (f'"{conda_path}"' + " install -y -k pip git --solver=libmamba", True),
        (f'"{conda_path}"' + " update -y -k --all --solver=libmamba", True),
        ("pip install --no-input ffmpeg-downloader", True),
        ("ffdl install -U --add-path 6.0@full", True),
        ("pip install soundfile", True),
        (
            "pip install torchaudio==2.0.2+cu118 torch==2.0.1+cu118 torchvision --extra-index-url https://download.pytorch.org/whl/cu118",
            True,
        ),
        ("pip install -r requirements-allpip.txt", True),
        (
            "pip install --no-deps encodec flashy>=0.0.1 demucs audiolm_pytorch==1.1.4 fairseq@https://github.com/Sharrnah/fairseq/releases/download/v0.12.4/fairseq-0.12.4-cp310-cp310-win_amd64.whl",
            True,
        ),
    ]
    bark_commands = [
        ("git clone https://github.com/JonathanFly/bark.git", True),
    ]

    # update from git if bark directory exists
    if BARK_DIR.exists():
        os.chdir(str(BARK_DIR))
        run_conda_cmd("git fetch", assert_success=True, dry_run=dry_run)
        run_conda_cmd("git pull", assert_success=True, dry_run=dry_run)

    os.chdir(str(SCRIPT_DIR))
    commands = base_commands if BARK_DIR.exists() else base_commands + bark_commands

    for cmd, assert_success in commands:
        run_conda_cmd(cmd, assert_success=assert_success, dry_run=dry_run)

    print(
        f"\n\nClose any open text terminals, and then click on the START_BARK_INFINITY.bat file in a new window. This seems to be necessary for FFMPEG to be detected after installation.\n\nIf you have trouble, you can try TROUBLESHOOT_BARK_INFINITY.bat\n\nRemember, if you use this terminal, you will have to type 'conda deactivate' first."
    )
    run_cmd(f'"{conda_path}"' + " deactivate", assert_success=False, dry_run=dry_run)


def launch_webui():
    os.chdir(str(BARK_DIR))

    """
    run_conda_cmd("git fetch", assert_success=True)
    run_conda_cmd("git checkout installer_test", assert_success=True)
    run_conda_cmd("git pull", assert_success=True)
    """

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

    check_env(args.dry_run)

    if not args.update and (not BARK_DIR.exists() or True):
        install_dependencies(args.dry_run)
        os.chdir(str(SCRIPT_DIR))
