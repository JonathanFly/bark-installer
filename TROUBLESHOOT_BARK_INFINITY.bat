@echo off

cd /D "%~dp0"

set PATH=%PATH%;%SystemRoot%\system32

echo "%CD%"| findstr /C:" " >nul && echo This script relies on Miniconda which can not be silently installed under a path with spaces. && goto end

@rem fix failed install when installing to a separate drive
set TMP=%cd%\installer_files
set TEMP=%cd%\installer_files

@rem config
set CONDA_ROOT_PREFIX=%cd%\installer_files\conda
set INSTALL_ENV_DIR=%cd%\installer_files\env

@rem environment isolation
set PYTHONNOUSERSITE=1
set PYTHONPATH=
set PYTHONHOME=
set "CUDA_PATH=%INSTALL_ENV_DIR%"
set "CUDA_HOME=%CUDA_PATH%"

echo -
echo -----START BARK MANUALLY------
echo Type 'cd bark' to enter the bark directory.
echo Type 'python bark_perform.py' to run the CLI.
echo Type 'python bark_webui.py' to run the GUI.
echo -
echo -----Manual Updates------

echo Type 'conda install -n base -y conda-libmamba-solver' to add mamba solver, if you are gettitng a mamba solver message.
echo Type 'conda update -y -n base conda' to update conda.
echo Type 'conda update -y --all --solver=libmamba' to update all packages.
echo Type 'conda clean --all' to free up disk space from unused versions.
echo type 'ffdl install -U --add-path' to try to reinstall ffmpeg if you have issues with it.
echo type 'pip install -r requirements-allpip.txt' to try to manually install pip requirements.

echo Type 'conda env update -y -f environment-cuda-installer.yml --prune --solver=libmamba' to update your env manually, if the .yml changed.
echo Type 'cd bark' to enter the bark directory and then 'git pull' to update the repo code.
echo -
echo -----Still Not Working?------
echo Go ahead and @ me on the Bark Official Discord, username "Jonathan Fly" jonathanfly. 
echo My Discord is always silent, don't worry about waking me up or anything, any time is fine.

echo -
echo -----How do I get out of here? ------
echo Type 'conda deactivate' to exit this environment and go back to normal terminal.
echo -

@rem activate installer env
call "%CONDA_ROOT_PREFIX%\condabin\conda.bat" activate "%INSTALL_ENV_DIR%" || ( echo. && echo Miniconda hook not found. && goto end )

@rem enter commands
cmd /k "%*"

Echo If there is an error, take note of it here.
PAUSE >nul
:end
pause
