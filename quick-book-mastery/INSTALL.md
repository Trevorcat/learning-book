# Quick Book Mastery Skill 安装指南

本 Skill 使用 `uv` 管理虚拟环境，并集成了 PaddleOCR 用于扫描版 PDF 的文字识别。

## 📋 系统要求

- **操作系统**: Windows 10/11, macOS, Linux
- **Python**: 3.8 或更高版本
- **内存**: 建议 4GB+（OCR 需要）
- **磁盘空间**: 约 2GB（包含模型文件）

## 🚀 快速安装

### 方式 1: 自动安装（推荐）

```bash
cd ~/.agents/skills/quick-book-mastery/scripts
python install.py
```

安装脚本会自动：
1. 检查并安装 `uv`（Python 包管理器）
2. 创建虚拟环境 (`.venv`)
3. 安装所有依赖（pdfplumber, paddleocr, PyMuPDF 等）
4. 下载 OCR 中文模型
5. 创建激活脚本

### 方式 2: 手动安装

如果你已经安装了 `uv`：

```bash
# 1. 创建虚拟环境
uv venv .venv

# 2. 激活环境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. 安装依赖
uv pip install pdfplumber paddlepaddle paddleocr pymupdf Pillow

# 4. 验证安装
python -c "from paddleocr import PaddleOCR; print('OK')"
```

## 🔧 使用虚拟环境

### 激活环境

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -File scripts/activate.ps1
```

**Windows (CMD):**
```cmd
scripts\activate.bat
```

**macOS/Linux:**
```bash
source scripts/activate.sh
```

### 使用脚本

激活环境后，可以直接运行脚本：

```bash
# 获取 PDF 概览
python scripts/pdf_reader.py book.pdf --overview

# OCR 扫描版 PDF
python scripts/pdf_reader.py book.pdf --toc --ocr
```

## 📖 使用 OCR 功能

### 自动检测

脚本会自动检测 PDF 类型：
- **文本型 PDF**: 直接提取文字
- **扫描型 PDF**: 自动启用 OCR

### 强制 OCR

如果自动检测不准确，可以强制使用 OCR：

```bash
python scripts/pdf_reader.py book.pdf --pages 1-10 --ocr
```

### 多语言支持

PaddleOCR 支持多种语言：

```bash
# 中文（默认）
python scripts/pdf_reader.py book.pdf --ocr --ocr-lang ch

# 英文
python scripts/pdf_reader.py book.pdf --ocr --ocr-lang en

# 日文
python scripts/pdf_reader.py book.pdf --ocr --ocr-lang japan
```

支持的语言代码：
| 语言 | 代码 |
|------|------|
| 中文简体 | ch |
| 中文繁体 | ch_tra |
| 英文 | en |
| 日文 | japan |
| 韩文 | korean |
| 德文 | german |
| 法文 | french |

## 🐛 故障排除

### 问题 1: "uv 未找到"

**解决**: 手动安装 uv
```bash
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 问题 2: "PaddleOCR 初始化失败"

**解决**: 模型会自动下载，如果失败可以手动下载：
```python
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=True)
```

### 问题 3: OCR 结果不准确

**解决**: 提高分辨率
```bash
python scripts/pdf_reader.py book.pdf --ocr --dpi 400
```

### 问题 4: 内存不足

**解决**: 分页处理
```bash
# 一次只 OCR 一页
python scripts/pdf_reader.py book.pdf --pages 1 --ocr
```

## 📁 目录结构

安装完成后，Skill 目录结构如下：

```
quick-book-mastery/
├── SKILL.md                 # Skill 主文件
├── INSTALL.md              # 本文件
├── .skill_config.json      # 安装配置（自动生成）
├── .venv/                  # 虚拟环境（自动生成）
│   ├── Scripts/            # Windows 可执行文件
│   └── ...
└── scripts/
    ├── install.py          # 安装脚本
    ├── pdf_reader.py       # PDF 阅读器（支持 OCR）
    ├── book_analyzer.py    # 书籍分析器
    ├── venv_manager.py     # 虚拟环境管理
    ├── activate.ps1        # Windows PowerShell 激活
    ├── activate.bat        # Windows CMD 激活
    └── activate.sh         # macOS/Linux 激活
```

## 🔄 更新依赖

```bash
# 激活环境
source scripts/activate.sh  # 或 .ps1 / .bat

# 更新包
uv pip install --upgrade paddleocr pdfplumber
```

## 🗑️ 卸载

直接删除 Skill 目录即可：

```bash
rm -rf ~/.agents/skills/quick-book-mastery
```

## 💡 提示

1. **首次 OCR 较慢**: 首次使用会自动下载模型（约 100MB），请保持网络畅通
2. **CPU 占用高**: OCR 是计算密集型任务，建议关闭其他大型程序
3. **模型缓存**: 模型会下载到 `~/.paddleocr`，不会重复下载

## 📚 参考链接

- [PaddleOCR GitHub](https://github.com/PaddlePaddle/PaddleOCR)
- [uv 文档](https://github.com/astral-sh/uv)
- [PyMuPDF 文档](https://pymupdf.readthedocs.io/)
