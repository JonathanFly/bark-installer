import argparse
import glob
import os
import shutil
import site
import subprocess
import sys

script_dir = os.getcwd()
conda_env_path = os.path.join(script_dir, "installer_files", "env")


# CMD_FLAGS = '--share'

CMD_FLAGS = ""

"""
# Gradio flags

--share               Enable share setting.
--user USER           User for authentication.
--password PASSWORD   Password for authentication.
--listen              Server name setting.
--server_port SERVER_PORT
                    Port setting.
--no-autolaunch       Disable automatic opening of the app in browser.
--debug               Enable detailed error messages and extra outputs.
--incolab             Default for Colab.
"""


def run_cmd(
    cmd, assert_success=False, environment=False, capture_output=False, env=None
):
    # Use the conda environment
    if environment:
        if sys.platform.startswith("win"):
            conda_bat_path = os.path.join(
                script_dir, "installer_files", "conda", "condabin", "conda.bat"
            )
            cmd = (
                '"'
                + conda_bat_path
                + '" activate "'
                + conda_env_path
                + '" >nul && '
                + cmd
            )
        else:
            conda_sh_path = os.path.join(
                script_dir, "installer_files", "conda", "etc", "profile.d", "conda.sh"
            )
            cmd = (
                '. "'
                + conda_sh_path
                + '" && conda activate "'
                + conda_env_path
                + '" && '
                + cmd
            )

    # Run shell commands
    print(f"Running command: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=capture_output, env=env)

    # Assert the command ran successfully
    if assert_success and result.returncode != 0:
        print(
            "Command '"
            + cmd
            + "' failed with exit status code '"
            + str(result.returncode)
            + "'. Exiting..."
        )
        sys.exit()

    return result


def check_env():
    # If we have access to conda, we are probably in an environment
    conda_exist = (
        run_cmd("conda", environment=True, capture_output=True).returncode == 0
    )
    if not conda_exist:
        print("Conda is not installed. Exiting...")
        sys.exit()

    # Ensure this is a new environment and not the base environment
    if os.environ["CONDA_DEFAULT_ENV"] == "base":
        print("Create an environment for this project and activate it. Exiting...")
        sys.exit()


def launch_webui():
    os.chdir("bark")

    """
    run_cmd(
        "git fetch",
        assert_success=True,
        environment=True,
    )

    run_cmd(
        "git checkout installer_test",
        assert_success=True,
        environment=True,
    )
    run_cmd(
        "git pull",
        assert_success=True,
        environment=True,
    )
    """
    run_cmd(f"python bark_webui.py {CMD_FLAGS}", environment=True)


if __name__ == "__main__":
    # Verifies we are in a conda environment
    check_env()

    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Update the web UI.")
    args = parser.parse_args()

    os.chdir(script_dir)
    launch_webui()
