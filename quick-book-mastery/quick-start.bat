@echo off
chcp 65001 >nul
echo ================================================
echo   Quick Book Mastery Skill - 快速启动
echo ================================================
echo.

set "SKILL_DIR=%~dp0"
set "VENV_PATH=%SKILL_DIR%.venv"

:: 检查虚拟环境
if not exist "%VENV_PATH%\Scripts\python.exe" (
    echo [首次使用] 正在安装依赖...
    echo.
    python "%SKILL_DIR%scripts\install.py"
    if errorlevel 1 (
        echo 安装失败，请检查错误信息
        pause
        exit /b 1
    )
)

echo 请选择操作:
echo.
echo  1. 获取 PDF 概览 (--overview)
echo  2. 提取目录 (--toc)
echo  3. 提取目录 + OCR (--toc --ocr)
echo  4. 读取指定页 (--pages)
echo  5. 搜索关键词 (--search)
echo  6. 生成大纲 (--outline)
echo  7. 退出
echo.

set /p choice="输入选项 (1-7): "

if "%choice%"=="7" exit /b 0

echo.
echo 请输入 PDF 文件路径（可拖放文件到窗口）:
set /p pdf_path="PDF 路径: "

:: 去除可能的引号
set pdf_path=%pdf_path:"=%

if not exist "%pdf_path%" (
    echo 错误: 文件不存在
    pause
    exit /b 1
)

echo.
echo 正在处理，请稍候...
echo.

set "PYTHON=%VENV_PATH%\Scripts\python.exe"
set "READER=%SKILL_DIR%scripts\pdf_reader.py"

if "%choice%"=="1" (
    "%PYTHON%" "%READER%" "%pdf_path%" --overview
) else if "%choice%"=="2" (
    "%PYTHON%" "%READER%" "%pdf_path%" --toc
) else if "%choice%"=="3" (
    "%PYTHON%" "%READER%" "%pdf_path%" --toc --ocr
) else if "%choice%"=="4" (
    set /p pages="输入页码范围 (如: 10-20): "
    "%PYTHON%" "%READER%" "%pdf_path%" --pages %pages%
) else if "%choice%"=="5" (
    set /p keyword="输入搜索关键词: "
    "%PYTHON%" "%READER%" "%pdf_path%" --search "%keyword%"
) else if "%choice%"=="6" (
    "%PYTHON%" "%READER%" "%pdf_path%" --outline
) else (
    echo 无效选项
)

echo.
echo ================================================
pause
