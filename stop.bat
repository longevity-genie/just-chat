@echo off
setlocal enabledelayedexpansion

:: Script to stop Docker Compose for Windows
:: WARNING: This script is experimental

echo WARNING: This script is experimental. If you encounter issues,
echo you can always use standard Docker commands directly:
echo    docker compose down [--volumes]
echo.

:: Function to display help message
:show_help
    echo Usage: %0 [OPTIONS]
    echo.
    echo Stop the just-chat application containers
    echo.
    echo Options:
    echo   -h, --help      Show this help message
    echo   -v, --volumes   Remove volumes as well
    echo.
    echo Examples:
    echo   %0              # Stop containers
    echo   %0 --volumes    # Stop containers and remove volumes
    echo.
    exit /b

:: Default options
set "VOLUMES_FLAG="

:: Process command line arguments
:parse_args
    if "%~1" == "" goto :end_parse_args
    if "%~1" == "-h" (
        call :show_help
        exit /b 0
    )
    if "%~1" == "--help" (
        call :show_help
        exit /b 0
    )
    if "%~1" == "-v" (
        set "VOLUMES_FLAG=--volumes"
        shift
        goto :parse_args
    )
    if "%~1" == "--volumes" (
        set "VOLUMES_FLAG=--volumes"
        shift
        goto :parse_args
    )
    echo Unknown option: %~1
    echo Use -h or --help for usage information
    exit /b 1
:end_parse_args

echo Stopping just-chat application...
echo ---------------------------------------------------------------------

:: Check if WSL is installed and has Docker
wsl --list >nul 2>nul
if %ERRORLEVEL% == 0 (
    wsl command -v docker >nul 2>nul
    if %ERRORLEVEL% == 0 (
        echo Using Docker via WSL
        :: Use Docker through WSL
        wsl bash -c "cd \"%CD%\" && docker compose down %VOLUMES_FLAG%"
        exit /b
    )
)

:: Check if Docker is installed on Windows
where docker >nul 2>nul
if %ERRORLEVEL% == 0 (
    echo Using Docker for Windows
    :: Stop containers
    docker compose down %VOLUMES_FLAG%
) else (
    :: If Docker is not available, try Podman
    where podman >nul 2>nul
    if %ERRORLEVEL% == 0 (
        echo Docker not found, falling back to Podman
        :: Stop containers using Podman
        podman-compose down %VOLUMES_FLAG%
    ) else (
        echo Error: Neither Docker nor Podman is installed or in PATH
        exit /b 1
    )
)
