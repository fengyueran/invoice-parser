@echo off
python --version
if %ERRORLEVEL% neq 0 (
    echo "Python is not installed, please install Python first."
    pause
    exit /b 1
)


python invoice-parser.py
if %ERRORLEVEL% neq 0 (
    echo "PDF extraction failed."
    pause
    exit /b 1
)


echo *****Invoice information extraction successful, the result has been exported to the output.xlsx file.*****

pause