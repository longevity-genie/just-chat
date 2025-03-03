@echo off
setlocal enabledelayedexpansion

:: Script to start Docker Compose with current user permissions for Windows

:: Function to display help message
:show_help
    echo Usage: %0 [OPTIONS]
    echo.
    echo Start the just-chat application using Docker or Podman
    echo.
    echo Options:
    echo   -d, --detach    Run containers in the background
    echo   -h, --help      Show this help message
    echo.
    echo Examples:
    echo   %0              # Run in foreground mode
    echo   %0 --detach     # Run in background mode
    echo.
    exit /b

:: Default to attached mode
set "DETACH_MODE="

:: Process command line arguments
:parse_args
    if "%~1" == "" goto :end_parse_args
    if "%~1" == "-d" (
        set "DETACH_MODE=-d"
        shift
        goto :parse_args
    )
    if "%~1" == "--detach" (
        set "DETACH_MODE=-d"
        shift
        goto :parse_args
    )
    if "%~1" == "-h" (
        call :show_help
        exit /b 0
    )
    if "%~1" == "--help" (
        call :show_help
        exit /b 0
    )
    echo Unknown option: %~1
    echo Use -h or --help for usage information
    exit /b 1
:end_parse_args

echo Starting just-chat application...
echo Will attempt to run using Docker or fall back to Podman if available
echo ---------------------------------------------------------------------
echo WARNING: This script is experimental. For standard usage, you can simply run:
echo    docker compose up
echo    or
echo    docker compose up -d    (for detached mode)
echo ---------------------------------------------------------------------

:: Check if WSL is installed and has Docker
wsl --list >nul 2>nul
if %ERRORLEVEL% == 0 (
    wsl command -v docker >nul 2>nul
    if %ERRORLEVEL% == 0 (
        echo Using Docker via WSL
        if defined DETACH_MODE (
            echo Running in detached mode
        )
        :: Use Docker through WSL with appropriate user permissions
        wsl bash -c "cd \"%CD%\" && USER_ID=$(id -u) GROUP_ID=$(id -g) docker compose up %DETACH_MODE%"
        exit /b
    )
)

:: Check if Docker is installed on Windows
where docker >nul 2>nul
if %ERRORLEVEL% == 0 (
    echo Using Docker for Windows
    if defined DETACH_MODE (
        echo Running in detached mode
    )
    :: Windows equivalent of setting user permissions
    docker compose up %DETACH_MODE%
) else (
    :: If Docker is not available, try Podman
    where podman >nul 2>nul
    if %ERRORLEVEL% == 0 (
        echo Docker not found, falling back to Podman
        if defined DETACH_MODE (
            echo Running in detached mode
        )
        :: Windows equivalent of setting user permissions
        podman-compose up %DETACH_MODE%
    ) else (
        echo Error: Neither Docker nor Podman is installed or in PATH
        exit /b 1
    )
)
