#!/bin/bash
# Quick Book Mastery Skill - 快速启动脚本 (macOS/Linux)

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SKILL_DIR/.venv"
PYTHON_EXE="$VENV_PATH/bin/python"
READER_SCRIPT="$SKILL_DIR/scripts/pdf_reader.py"

# 颜色
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

show_header() {
    echo ""
    echo -e "${CYAN}================================================${NC}"
    echo -e "${CYAN}  Quick Book Mastery Skill - 快速启动${NC}"
    echo -e "${CYAN}================================================${NC}"
    echo ""
}

check_venv() {
    if [ ! -f "$PYTHON_EXE" ]; then
        echo "[首次使用] 正在安装依赖..."
        echo ""
        python3 "$SKILL_DIR/scripts/install.py"
        if [ $? -ne 0 ]; then
            echo "安装失败，请检查错误信息"
            read -p "按 Enter 键退出"
            exit 1
        fi
    fi
}

show_menu() {
    echo "请选择操作:"
    echo ""
    echo "  1. 获取 PDF 概览 (--overview)"
    echo "  2. 提取目录 (--toc)"
    echo "  3. 提取目录 + OCR (--toc --ocr)"
    echo "  4. 读取指定页 (--pages)"
    echo "  5. 搜索关键词 (--search)"
    echo "  6. 生成大纲 (--outline)"
    echo "  7. 退出"
    echo ""
}

get_pdf_path() {
    echo "请输入 PDF 文件路径:"
    read -r pdf_path
    
    # 去除可能的引号
    pdf_path="${pdf_path%\"}"
    pdf_path="${pdf_path#\"}"
    
    if [ ! -f "$pdf_path" ]; then
        echo "错误: 文件不存在"
        read -p "按 Enter 键退出"
        exit 1
    fi
    
    echo "$pdf_path"
}

# 主程序
show_header
check_venv

running=true
while $running; do
    show_menu
    read -p "输入选项 (1-7): " choice
    
    case $choice in
        1)
            pdf_path=$(get_pdf_path)
            echo ""
            echo -e "${CYAN}正在处理...${NC}"
            "$PYTHON_EXE" "$READER_SCRIPT" "$pdf_path" --overview
            ;;
        2)
            pdf_path=$(get_pdf_path)
            echo ""
            echo -e "${CYAN}正在处理...${NC}"
            "$PYTHON_EXE" "$READER_SCRIPT" "$pdf_path" --toc
            ;;
        3)
            pdf_path=$(get_pdf_path)
            echo ""
            echo -e "${YELLOW}正在处理（OCR 模式，请稍候）...${NC}"
            "$PYTHON_EXE" "$READER_SCRIPT" "$pdf_path" --toc --ocr
            ;;
        4)
            pdf_path=$(get_pdf_path)
            read -p "输入页码范围 (如: 10-20): " pages
            echo ""
            echo -e "${CYAN}正在处理...${NC}"
            "$PYTHON_EXE" "$READER_SCRIPT" "$pdf_path" --pages "$pages"
            ;;
        5)
            pdf_path=$(get_pdf_path)
            read -p "输入搜索关键词: " keyword
            echo ""
            echo -e "${CYAN}正在搜索...${NC}"
            "$PYTHON_EXE" "$READER_SCRIPT" "$pdf_path" --search "$keyword"
            ;;
        6)
            pdf_path=$(get_pdf_path)
            echo ""
            echo -e "${CYAN}正在生成大纲...${NC}"
            "$PYTHON_EXE" "$READER_SCRIPT" "$pdf_path" --outline
            ;;
        7)
            running=false
            continue
            ;;
        *)
            echo "无效选项"
            ;;
    esac
    
    if $running; then
        echo ""
        echo -e "${CYAN}================================================${NC}"
        read -p "按 Enter 键继续"
        clear
        show_header
    fi
done

echo -e "${GREEN}再见！${NC}"
