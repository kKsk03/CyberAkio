@echo off
REM 检查是否安装Python
python --version >nul 2>&1

IF %ERRORLEVEL% EQU 0 (
    REM 如果找到Python，则运行bot.py
    python bot.py
) ELSE (
    echo Python 未安装，请先安装Python。
)
