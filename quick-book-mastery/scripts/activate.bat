@echo off
call "C:\Users\chenkejie\.claude\skills\learning-book\quick-book-mastery\.venv\Scripts\activate.bat"
if %errorlevel% == 0 (
    echo ✅ Skill 环境已激活
) else (
    echo ❌ 虚拟环境不存在，请先运行 install.py
)
