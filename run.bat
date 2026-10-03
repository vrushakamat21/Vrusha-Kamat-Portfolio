@echo off
echo ===============================================================
echo   Starting Vrusha Kamat Portfolio - Java Web Server
echo ===============================================================
echo.
javac PortfolioServer.java
if %ERRORLEVEL% NEQ 0 (
    echo Compilation failed. Make sure JDK is installed and on PATH.
    pause
    exit /b %ERRORLEVEL%
)
echo Compiled successfully! Launching server...
echo.
java PortfolioServer
pause
