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

echo ----- BARK INFINITY COMMAND LINE------
echo Type 'python bark_perform.py' to run the CLI.
echo Type 'python bark_perform.py --help' for options
echo Type 'conda deactivate' to exit this environment and go back to normal terminal.
echo ----- Example usage:
echo python bark_perform.py --history_prompt "bark_infinity\assets\prompts\en_fiery.npz" --text_prompt "I refuse to answer that question on the grounds that I don't know the answer."

echo ----- read prompts from text file
echo `python bark_perform.py --prompt_file myprompts.txt --split_input_into_separate_prompts_by string --split_input_into_separate_prompts_by_value AAAAA --output_dir myprompts_samples`


echo -

@rem activate installer env
call "%CONDA_ROOT_PREFIX%\condabin\conda.bat" activate "%INSTALL_ENV_DIR%" && cd bark || ( echo. && echo Miniconda hook not found. && goto end )

@rem enter commands
cmd /k "%*"

Echo If there is an error, take note of it here.
PAUSE >nul
:end
pause
