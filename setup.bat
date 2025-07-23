@echo off
REM Force script to run from the directory where the script is located
cd /d "%~dp0"
echo ================================================
echo Django Project Setup & Management
+ Tailwind CSS
===============================================

REM Check if virtual environment exists
if not exist "wvenv" (
    echo ERROR: Virtual environment not found!
    echo Please run install.bat first.
    pause
    exit /b 1
)

call wvenv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

:menu
echo.
echo 1. Run Django development server
echo 2. Create new Django app
echo 3. Start Tailwind CSS (watch mode)
echo 4. Build Tailwind CSS (production)
echo 5. Run BOTH Django server & Tailwind (2 windows)
echo 6. Make migrations
echo 7. Apply migrations
echo 8. Create superuser
echo 9. Collect static files
echo 0. Exit
echo.
set /p choice="Enter your choice (0-9): "

if "%choice%"=="1" goto runserver
if "%choice%"=="2" goto createapp
if "%choice%"=="3" goto tailwindstart
if "%choice%"=="4" goto tailwindbuild
if "%choice%"=="5" goto both
if "%choice%"=="6" goto makemigrations
if "%choice%"=="7" goto migrate
if "%choice%"=="8" goto superuser
if "%choice%"=="9" goto collectstatic
if "%choice%"=="0" goto exit

echo Invalid choice. Try again.
goto menu

:runserver
echo Starting Django development server...
python manage.py runserver
goto menu

:createapp
echo.
set /p appname="Enter new app name: "
if "%appname%"=="" (
    echo App name cannot be empty!
    goto menu
)
python manage.py startapp %appname%
if errorlevel 1 (
    echo Failed to create app!
    pause
    goto menu
)

REM Add app to INSTALLED_APPS in settings.py (robust, no duplicates)
python add_to_installed_apps.py %appname%
echo If successful, '%appname%' was added to INSTALLED_APPS in settings.py

REM Create starter urls.py for the app
 echo Creating starter urls.py for %appname%...
 echo from django.urls import path^, include > %appname%\urls.py
 echo from . import views >> %appname%\urls.py
 echo urlpatterns = [ >> %appname%\urls.py
 echo     path('', views.index, name='index'), >> %appname%\urls.py
 echo ] >> %appname%\urls.py

REM Create starter views.py for the app (if not exists)
 if not exist %appname%\views.py (
     echo from django.http import HttpResponse > %appname%\views.py
     echo def index(request): >> %appname%\views.py
     echo     return HttpResponse('Hello from %appname%!') >> %appname%\views.py
 ) else (
     echo. >> %appname%\views.py
     echo def index(request): >> %appname%\views.py
     echo     return HttpResponse('Hello from %appname%!') >> %appname%\views.py
 )

REM Add app urls to main urls.py if not already included (after Core.urls)
python add_to_main_urls.py %appname%
echo If successful, '%appname%' urls are included in main urls.py
pause
goto menu

tailwindstart:
 echo Ensuring Node.js dependencies are installed...
 pushd theme\static_src
 npm install
 echo Starting Tailwind CSS in watch mode...
 npx tailwindcss --postcss -i ./src/styles.css -o ../static/css/dist/styles.css -w
 popd
 goto menu

tailwindbuild:
 echo Ensuring Node.js dependencies are installed...
 pushd theme\static_src
 npm install
 echo Building Tailwind CSS for production...
 npx tailwindcss --postcss -i ./src/styles.css -o ../static/css/dist/styles.css --minify
 popd
 goto menu

:both
 echo Opening Tailwind CSS in a new window...
 start "Tailwind CSS" cmd /k "cd /d %cd% && call wvenv\Scripts\activate.bat && pushd theme\static_src && npm install && npx tailwindcss --postcss -i ./src/styles.css -o ../static/css/dist/styles.css -w && popd"
 timeout /t 2 >nul
 echo Starting Django development server...
 python manage.py runserver
 goto menu

:makemigrations
echo Making migrations...
python manage.py makemigrations
goto menu

:migrate
echo Applying migrations...
python manage.py migrate
goto menu

:superuser
echo Creating superuser...
python manage.py createsuperuser
goto menu

:collectstatic
echo Collecting static files...
python manage.py collectstatic --noinput
goto menu

:exit
echo Goodbye!
pause
exit /b 0
