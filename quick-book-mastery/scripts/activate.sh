#!/bin/bash
VENV_PATH="C:\Users\chenkejie\.claude\skills\learning-book\quick-book-mastery\.venv"

if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"
    echo "✅ Skill 环境已激活"
else
    echo "❌ 虚拟环境不存在，请先运行 install.py"
fi
