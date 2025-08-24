@echo off
rem ---[ Conda 虚拟环境激活脚本 for Windows ]---
rem
rem 脚本功能：
rem 1. 检查是否安装 Conda。
rem 2. 如果虚拟环境不存在，则提示用户创建。
rem 3. 激活指定的虚拟环境。
rem
rem ------------------------------------

rem --- 配置部分 ---
set CONDA_ENV_NAME=map_of_XJTU_MED     rem 虚拟环境名称
set ENV_FILE=environment_map_of_XJTU_MED.yml rem 环境依赖文件名 (用于提示用户)

echo.
echo ------------------------------------------------------------------
echo            正在尝试激活 Conda 虚拟环境 "%CONDA_ENV_NAME%"...
echo ------------------------------------------------------------------
echo.

rem 检查 Conda 是否安装并可用
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo 错误：未检测到 Conda（Miniconda/Anaconda）。
    echo 请访问以下链接下载并安装 Miniconda 或 Anaconda：
    echo   https://docs.anaconda.com/free/miniconda/miniconda-install/
    echo 安装完成后，请重新运行本脚本。
    echo.
    pause
    exit /b 1
)

rem 检查虚拟环境是否存在
conda env list | findstr /i "%CONDA_ENV_NAME%" >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo 警告：虚拟环境 "%CONDA_ENV_NAME%" 不存在！
    echo 请先通过以下命令创建它：
    echo   conda env create -f "%ENV_FILE%"
    echo.
    echo 创建完成后，请再次运行本脚本。
    echo.
    pause
    exit /b 1
)

rem 激活虚拟环境
echo 找到 Conda 的基本路径，并激活环境...
rem 为了在当前 cmd 窗口激活环境，必须使用 call 命令
for /f "tokens=*" %%i in ('conda info --base') do set CONDA_BASE_PATH=%%i
call "%CONDA_BASE_PATH%\Scripts\activate.bat" %CONDA_ENV_NAME%

if %errorlevel% neq 0 (
    echo.
    echo 错误：激活虚拟环境失败！
    echo 请检查 Conda 安装是否完整，或虚拟环境名称 "%CONDA_ENV_NAME%" 是否拼写正确。
    echo.
    pause
    exit /b 1
)

echo.
echo ------------------------------------------------------------------
echo            虚拟环境 "%CONDA_ENV_NAME%" 已成功激活！
echo ------------------------------------------------------------------
echo.
pause
rem --- 结束 ---
