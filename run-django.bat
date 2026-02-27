@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo   Technolnstrument — Django
echo ========================================
echo.

REM 1) py (лаунчер), 2) полный путь к Python313, 3) python из PATH
set PY=
where py >nul 2>&1
if %errorlevel% equ 0 (
  set PY=py
)
if not defined PY (
  if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    set "PY=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
  )
)
if not defined PY (
  if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
  )
)
if not defined PY (
  where python >nul 2>&1
  if %errorlevel% equ 0 (
    set PY=python
  )
)
if not defined PY (
  echo Python не найден. Установите с python.org и добавьте в PATH.
  pause
  exit /b 1
)

echo Проверка Django...
%PY% -c "import django" 2>nul
if %errorlevel% neq 0 (
  echo Установка зависимостей...
  %PY% -m pip install -r requirements.txt
)

echo.
echo Запуск сервера: http://127.0.0.1:8000/
echo Остановка: Ctrl+C
echo.

%PY% manage.py runserver

pause
