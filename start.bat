@echo off & title AternosServerManager bot by chepchek tg: @UserNotZFound & color B

python -V | find /v "Python" >NUL 2>NUL && (goto :PYTHON_DOES_NOT_EXIST)
python -V | find "Python"    >NUL 2>NUL && (goto :PYTHON_DOES_EXIST)

:MAIN
if not exist %~dp0venv\ (
    echo.
    echo Warn^: File  venv not found... Download requirements
    python -m venv venv
    call %~dp0venv\Scripts\activate.bat
)
if not exist %~dp0.env (
    cls
    echo.
    echo Error^: .env not found. Please create this file
    pause
    exit
)
call %~dp0venv\Scripts\activate.bat
python -m pip install -r requirements.txt
cls
color 2
echo. & echo. & echo.
echo the author of the bot @chepchek https://github.com/Chepchek
echo.
echo If you have any problems or suggestions: https://t.me/UserNotZFound
echo. & echo. & echo.
timeout 10
color F
python pooling.py
pause

:PYTHON_DOES_NOT_EXIST
color 4
cls
echo Python is not installed on your system.
pause


:PYTHON_VERSION_NOT_SUPPORTED
color 4
cls
echo Python version is not supported, please download python 3.7 or above
pause



:PYTHON_DOES_EXIST
for /f "delims=" %%V in ('python -V') do @set ver=%%V

set ver=%ver: =%
set ver=%ver:Python=%
set ver=%ver:~0,4%

set major=%ver%
set major=%major:~0,1%

set minor=%ver%
set minor=%minor:~2,3%

if %major% GEQ 3 (
    goto :MAIN
)
pause