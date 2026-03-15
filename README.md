# 📚 Quick Book Mastery

基于《如何阅读一本书》方法论的智能学习助手 Skill，支持 OCR 识别扫描版 PDF。

## ✨ 功能特点

- **四阶段学习流程**: 准备 → 概览 → 深入 → 巩固
- **OCR 集成**: 自动识别扫描版 PDF（使用 PaddleOCR）
- **Token 节省**: 策略性提取，避免整本书浪费 Token
- **虚拟环境**: 使用 uv 管理，隔离依赖
- **多语言支持**: 支持 80+ 种语言 OCR

## 🚀 一键安装

### Windows (PowerShell)
```powershell
irm https://raw.githubusercontent.com/Trevorcat/learning-book/main/install.ps1 | iex
```

### macOS / Linux
```bash
curl -fsSL https://raw.githubusercontent.com/Trevorcat/learning-book/main/install.sh | bash
```

### 手动安装
```bash
git clone https://github.com/Trevorcat/learning-book.git
cd learning-book
python install.py
```

## 📖 使用方法

### 方式 1: 快速启动
```bash
cd quick-book-mastery
./quick-start.ps1  # Windows
# 或
./quick-start.sh   # macOS/Linux
```

### 方式 2: 命令行
```bash
# 获取 PDF 概览（自动检测 PDF 类型）
python scripts/pdf_reader.py book.pdf --overview

# OCR 扫描版 PDF
python scripts/pdf_reader.py book.pdf --toc --ocr

# 搜索关键词
python scripts/pdf_reader.py book.pdf --search "Python"

# 读取特定页
python scripts/pdf_reader.py book.pdf --pages 10-20
```

## 📋 四阶段学习流程

| 阶段 | 时间 | 核心方法 |
|-----|------|---------|
| 准备 | 5-10 分钟 | 目标设定、先验知识激活 |
| 概览 | 10-15 分钟 | 检视阅读、框架构建 |
| 深入 | 15-30 分钟 | 费曼复述、主动回忆 |
| 巩固 | 5-10 分钟 | 间隔重复、行动计划 |

## 🔧 支持的 Kimi Code CLI 技能目录

安装后，Skill 会自动安装到以下位置之一：
- `~/.agents/skills/quick-book-mastery/`
- `~/.kimi/skills/quick-book-mastery/`

## 📁 仓库结构

```
learning-book/
├── README.md                    # 本文件
├── install.sh                   # Linux/Mac 安装脚本
├── install.ps1                  # Windows 安装脚本
└── quick-book-mastery/          # Skill 目录
    ├── SKILL.md                 # Skill 主文件
    ├── INSTALL.md               # 详细安装文档
    ├── quick-start.ps1          # Windows 快速启动
    └── scripts/                 # 工具脚本
        ├── install.py           # 依赖安装
        ├── pdf_reader.py        # PDF 阅读器（含 OCR）
        ├── book_analyzer.py     # 书籍分析
        └── venv_manager.py      # 环境管理
```

## 🛠️ 技术栈

- **OCR 引擎**: [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) (百度开源)
- **包管理**: [uv](https://github.com/astral-sh/uv)
- **PDF 处理**: pdfplumber, PyMuPDF
- **虚拟环境**: Python venv

## 📝 使用方法示例

### 学习一本扫描版技术书籍

```bash
# 1. 一键安装
irm https://raw.githubusercontent.com/Trevorcat/learning-book/main/install.ps1 | iex

# 2. 运行快速启动器
quick-book-mastery/quick-start.ps1

# 3. 选择操作（如：提取目录 + OCR）
# 4. 输入 PDF 路径
# 5. 开始学习！
```

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- 《如何阅读一本书》作者：莫提默·艾德勒、查尔斯·范多伦
- PaddleOCR 团队
- Kimi Code CLI 团队
