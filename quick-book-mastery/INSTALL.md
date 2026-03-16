# Quick Book Mastery Skill 安装指南

本 Skill 使用 `uv` 管理虚拟环境，并集成了 **PaddleOCR 3.x** 用于扫描版 PDF 的文字识别（支持 CUDA 12 加速）。

## 📋 系统要求

- **操作系统**: Windows 10/11, macOS, Linux
- **Python**: 3.8 - 3.12（推荐 3.12）
- **CUDA**: 12.0+（如需 GPU 加速）
- **内存**: 建议 8GB+（OCR 需要）
- **磁盘空间**: 约 3GB（包含模型文件）
- **GPU**: NVIDIA GPU，计算能力 6.0+（可选，用于加速）

## 🚀 快速安装

### 方式 1: 自动安装（推荐）

```bash
cd ~/.agents/skills/quick-book-mastery/scripts
python install.py
```

安装脚本会自动：
1. 检查并安装 `uv`（Python 包管理器）
2. 创建虚拟环境 (`.venv`)
3. 安装 **PaddlePaddle 3.0 + CUDA 12** 支持
4. 安装 **PaddleOCR 3.x**
5. 安装其他依赖（pdfplumber, PyMuPDF 等）
6. 创建激活脚本

### 方式 2: 手动安装

如果你已经安装了 `uv`：

```bash
# 1. 创建虚拟环境（使用 Python 3.12）
uv venv -p python3.12 .venv

# 2. 激活环境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. 安装 PaddlePaddle 3.0 (CUDA 12.6 版本)
uv pip install paddlepaddle-gpu==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/

# 4. 安装 PaddleOCR 3.x
uv pip install paddleocr>=3.0

# 5. 安装其他依赖
uv pip install pdfplumber pymupdf Pillow

# 6. 验证安装
python -c "import paddle; print(f'Paddle: {paddle.__version__}'); print(f'CUDA: {paddle.version.cuda()}')"
```

## 🔧 验证安装

### 检查 GPU 支持

```python
import paddle

print(f"PaddlePaddle 版本: {paddle.__version__}")
print(f"CUDA 可用: {paddle.is_compiled_with_cuda()}")
print(f"CUDA 版本: {paddle.version.cuda()}")
print(f"cuDNN 版本: {paddle.version.cudnn()}")

# 运行完整检查
paddle.utils.run_check()
```

预期输出：
```
PaddlePaddle 版本: 3.0.0
CUDA 可用: True
CUDA 版本: 12.6
cuDNN 版本: 9.5.1
Running verify PaddlePaddle program ...
PaddlePaddle works well on 1 GPU.
PaddlePaddle is installed successfully!
```

### 测试 OCR 功能

```python
from paddleocr import PaddleOCR

# 初始化 OCR（自动检测 GPU）
ocr = PaddleOCR(lang='ch')

# 测试识别
result = ocr.ocr('test_image.png')
print(f"识别到 {len(result[0]) if result and result[0] else 0} 个文本块")
```

## 📖 使用虚拟环境

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

# 读取指定页
python scripts/pdf_reader.py book.pdf --pages 10-20
```

## 🐛 故障排除

### 问题 1: "uv 未找到"

**解决**: 手动安装 uv
```bash
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 问题 2: "CUDA 不可用" 或 "No GPU found"

**解决**:
1. 检查 NVIDIA 驱动
```bash
nvidia-smi
```

2. 如果没有 GPU 或驱动问题，使用 CPU 版本：
```bash
uv pip install paddlepaddle
# 不使用 -gpu 后缀
```

3. 检查 CUDA 版本匹配：
```bash
nvcc --version  # 查看系统 CUDA 版本
```
确保安装的 paddlepaddle-gpu 版本与系统 CUDA 版本匹配：
- CUDA 12.6: `paddlepaddle-gpu==3.0.0` (cu126)
- CUDA 12.3: `paddlepaddle-gpu==3.0.0` (cu123)
- CUDA 11.8: `paddlepaddle-gpu==3.0.0` (cu118)

### 问题 3: "AttributeError: 'paddle.base.libpaddle.AnalysisConfig' object has no attribute 'set_optimization_level'"

**解决**: 这是 PaddleX 与 PaddlePaddle 版本的兼容性问题。

编辑文件：`.venv/Lib/site-packages/paddlex/inference/models/common/static_infer.py`

找到第 403 行，将：
```python
config.set_optimization_level(3)
```

改为：
```python
if hasattr(config, "set_optimization_level"):
    config.set_optimization_level(3)
```

### 问题 4: "OSError: [WinError 127] 找不到指定的程序"

**解决**: cuDNN 库缺失或版本不匹配。

1. 确保安装了正确版本的 cuDNN：
   - CUDA 12.x 需要 cuDNN 9.x

2. 如果已安装 cuDNN，检查环境变量：
```powershell
$env:CUDA_PATH
$env:PATH
```

3. 临时解决方案（将 cuDNN dll 复制到虚拟环境）：
```powershell
copy "C:\Program Files\NVIDIA\CUDNN\v9\bin\*.dll" .venv\Scripts\
```

### 问题 5: OCR 结果不准确

**解决**: 提高分辨率或调整参数
```bash
# 提高 DPI
python scripts/pdf_reader.py book.pdf --ocr --dpi 400

# 只 OCR 特定页面
python scripts/pdf_reader.py book.pdf --pages 10-15 --ocr
```

### 问题 6: 内存不足

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

# 更新 PaddlePaddle
uv pip install --upgrade paddlepaddle-gpu -i https://www.paddlepaddle.org.cn/packages/stable/cu126/

# 更新 PaddleOCR
uv pip install --upgrade paddleocr

# 更新其他依赖
uv pip install --upgrade pdfplumber pymupdf
```

## 🗑️ 卸载

直接删除 Skill 目录即可：

```bash
rm -rf ~/.agents/skills/quick-book-mastery
```

## 💡 提示

1. **首次 OCR 较慢**: 首次使用会自动下载模型（约 100-200MB），请保持网络畅通
2. **GPU 加速**: PaddleOCR 3.x 自动检测并使用 GPU，无需手动设置
3. **模型缓存**: 模型会下载到 `~/.paddlex`，不会重复下载
4. **CUDA 版本**: 如果系统 CUDA 版本与 PaddlePaddle 不匹配，可以使用 CPU 版本（去掉 `-gpu`）

## 📚 参考链接

- [PaddleOCR GitHub](https://github.com/PaddlePaddle/PaddleOCR)
- [PaddlePaddle 安装指南](https://www.paddlepaddle.org.cn/install/quick)
- [uv 文档](https://github.com/astral-sh/uv)
- [PyMuPDF 文档](https://pymupdf.readthedocs.io/)

## 🆕 更新日志

### v2.0 (2025-03-16)
- ✅ 升级 PaddleOCR 2.x → 3.x
- ✅ 支持 CUDA 12.x（原生支持，无需降级）
- ✅ 更新 PaddlePaddle 2.6 → 3.0
- ✅ 新增学习模式选择（快速模式/伴读模式）
- ✅ 优化 PDF 阅读器，支持 PaddleOCR 3.x API
