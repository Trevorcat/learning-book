#!/bin/bash
# Quick Book Mastery Skill - Linux/macOS 一键安装脚本
# 安装地址: https://github.com/Trevorcat/learning-book

set -e

# 配置
REPO_URL="https://github.com/Trevorcat/learning-book.git"
SKILL_NAME="quick-book-mastery"
INSTALL_DIR="$HOME/.agents/skills/$SKILL_NAME"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo -e "${CYAN}===============================================${NC}"
    echo -e "${CYAN}  Quick Book Mastery Skill - 一键安装${NC}"
    echo -e "${CYAN}===============================================${NC}"
    echo ""
}

check_command() {
    command -v "$1" >/dev/null 2>&1
}

install_git() {
    echo -e "${YELLOW}📦 Git 未安装，正在安装...${NC}"
    
    if check_command apt-get; then
        # Debian/Ubuntu
        sudo apt-get update
        sudo apt-get install -y git
    elif check_command yum; then
        # CentOS/RHEL
        sudo yum install -y git
    elif check_command dnf; then
        # Fedora
        sudo dnf install -y git
    elif check_command brew; then
        # macOS
        brew install git
    elif check_command pacman; then
        # Arch
        sudo pacman -S git --noconfirm
    else
        echo -e "${RED}❌ 无法自动安装 Git${NC}"
        echo "请手动安装 Git: https://git-scm.com/downloads"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Git 安装完成${NC}"
}

install_uv() {
    if ! check_command uv; then
        echo -e "${CYAN}📦 安装 uv (Python 包管理器)...${NC}"
        curl -LsSf https://astral.sh/uv/install.sh | sh
        # 添加到当前 shell 的 PATH
        export PATH="$HOME/.cargo/bin:$PATH"
    fi
}

install_skill() {
    print_header
    
    # 检查 Git
    if ! check_command git; then
        install_git
    fi
    
    echo -e "${GREEN}✅ Git 已安装${NC}"
    echo ""
    
    # 创建安装目录
    mkdir -p "$(dirname "$INSTALL_DIR")"
    
    # 如果已存在，先备份
    if [ -d "$INSTALL_DIR" ]; then
        BACKUP_NAME="${SKILL_NAME}-backup-$(date +%Y%m%d-%H%M%S)"
        echo -e "${YELLOW}📁 检测到已安装，备份到: $BACKUP_NAME${NC}"
        mv "$INSTALL_DIR" "$(dirname "$INSTALL_DIR")/$BACKUP_NAME"
    fi
    
    # 克隆仓库
    echo -e "${CYAN}📥 正在下载 Skill...${NC}"
    if git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"; then
        echo -e "${GREEN}✅ 下载完成${NC}"
    else
        echo -e "${RED}❌ 下载失败${NC}"
        exit 1
    fi
    
    echo ""
    echo -e "${CYAN}📦 正在安装依赖（这可能需要几分钟）...${NC}"
    
    # 进入 skill 目录
    cd "$INSTALL_DIR/quick-book-mastery"
    
    # 安装 uv
    install_uv
    
    # 运行安装脚本
    if [ -f "scripts/install.py" ]; then
        python3 scripts/install.py
    else
        echo -e "${YELLOW}⚠️ 安装脚本不存在，尝试手动安装...${NC}"
        
        # 创建虚拟环境
        uv venv .venv
        
        # 安装依赖
        VENV_PYTHON=".venv/bin/python"
        uv pip install --python "$VENV_PYTHON" pdfplumber paddlepaddle paddleocr pymupdf Pillow
    fi
    
    # 创建启动脚本软链接
    if check_command quick-book-mastery; then
        echo -e "${YELLOW}命令已存在，跳过创建软链接${NC}"
    else
        echo -e "${CYAN}创建快捷命令...${NC}"
        
        # 添加到 .bashrc 或 .zshrc
        SHELL_RC=""
        if [ -n "$ZSH_VERSION" ]; then
            SHELL_RC="$HOME/.zshrc"
        elif [ -n "$BASH_VERSION" ]; then
            SHELL_RC="$HOME/.bashrc"
        fi
        
        if [ -n "$SHELL_RC" ]; then
            echo "alias quick-book-mastery=\"$INSTALL_DIR/quick-book-mastery/quick-start.sh\"" >> "$SHELL_RC"
            echo -e "${GREEN}✅ 已添加到 $SHELL_RC${NC}"
            echo -e "${YELLOW}请运行: source $SHELL_RC${NC}"
        fi
    fi
    
    echo ""
    echo -e "${GREEN}===============================================${NC}"
    echo -e "${GREEN}  ✅ 安装完成！${NC}"
    echo -e "${GREEN}===============================================${NC}"
    echo ""
    echo -e "${CYAN}使用方法:${NC}"
    echo "  1. 快速启动:"
    echo -e "     ${YELLOW}$INSTALL_DIR/quick-book-mastery/quick-start.sh${NC}"
    echo ""
    echo "  2. 命令行使用:"
    echo -e "     ${YELLOW}cd $INSTALL_DIR/quick-book-mastery${NC}"
    echo -e "     ${YELLOW}.venv/bin/python scripts/pdf_reader.py <pdf> --overview${NC}"
    echo ""
    echo "  3. 在 Kimi Code CLI 中使用:"
    echo -e "     ${YELLOW}直接说: '帮我学习这本书'${NC}"
    echo ""
    echo -e "${GRAY}📖 文档: https://github.com/Trevorcat/learning-book${NC}"
    echo ""
}

# 运行安装
install_skill
