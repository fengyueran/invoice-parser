@echo off

REM 检查 pip 是否安装
pip --version
if %ERRORLEVEL% neq 0 (
    echo "pip is not installed. Please install pip first."
    pause
    exit /b 1
)

REM 安装 pdfplumber
pip install pdfplumber
if %ERRORLEVEL% neq 0 (
    echo "Failed to install pdfplumber."
    pause
    exit /b 1
)

REM 安装 pandas
pip install pandas
if %ERRORLEVEL% neq 0 (
    echo "Failed to install pandas."
    pause
    exit /b 1
)

REM 安装 openpyxl
pip install openpyxl
if %ERRORLEVEL% neq 0 (
    echo "Failed to install openpyxl."
    pause
    exit /b 1
)

echo "All dependencies installed successfully."
pause