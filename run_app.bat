@echo off
REM Run Streamlit app using the project's virtual environment Python
SET VENV_PY=%~dp0venv\Scripts\python.exe
IF EXIST "%VENV_PY%" (
	"%VENV_PY%" -m streamlit run app.py
) ELSE (
	echo Virtual environment python not found at %VENV_PY%
	echo Activate your venv or run streamlit with a Python that has the project dependencies installed.
)

