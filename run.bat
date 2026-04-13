@echo off
setlocal

:: Set the name of the virtual environment directory
set VENV_DIR=.venv

:: Check if the virtual environment directory exists
if not exist %VENV_DIR% (
    echo [INFO] Virtual environment not found. Creating one...
    python -m venv %VENV_DIR%
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment. Please ensure Python is installed and in your PATH.
        pause
        exit /b 1
    )
    
    echo [INFO] Activating virtual environment and installing dependencies...
    call %VENV_DIR%\Scripts\activate
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install requirements. Check your internet connection or requirements.txt.
        pause
        exit /b 1
    )
) else (
    echo [INFO] Activating existing virtual environment...
    call %VENV_DIR%\Scripts\activate
)

:: Run the Streamlit application
echo [INFO] Starting Smart Diet Nutrition Planner...
streamlit run src/app.py

:: Keep the window open if the app crashes
if errorlevel 1 (
    echo [ERROR] Application exited with an error.
    pause
)

endlocal
