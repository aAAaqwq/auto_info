@echo off
setlocal enabledelayedexpansion

echo Starting Vite dev server...
echo Press Ctrl+C to stop

REM 捕获Ctrl+C信号，清理后退出
cmd /c npm run dev

REM 退出后清理可能残留的进程
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173 :5174 :5175 :5176 :5177 :5178 2^>nul ^| findstr LISTENING') do (
    taskkill /F /PID %%a 2>nul
)

echo.
echo Vite dev server stopped
