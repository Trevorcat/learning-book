#!/usr/bin/env python3
"""
Quick Book Mastery Skill 安装脚本 (PaddleOCR 3.x + CUDA 12)

自动完成：
1. 检查并安装 uv（如果未安装）
2. 创建虚拟环境（Python 3.12）
3. 安装 PaddlePaddle 3.0 + CUDA 12
4. 安装 PaddleOCR 3.x
5. 安装其他依赖
6. 验证安装

使用方法:
    python install.py

要求:
    - Python 3.8-3.12
    - 网络连接（下载模型和依赖）
    - NVIDIA GPU + CUDA 12.x（可选，用于加速）

更新日志:
    v2.0 (2025-03-16): 升级 PaddleOCR 2.x → 3.x, 支持 CUDA 12
"""

import os
import subprocess
import sys
from pathlib import Path

# 配置
VENV_NAME = ".venv"
REQUIRED_PACKAGES = [
    "pdfplumber>=0.10.0",
    "pymupdf>=1.23.0",  # fitz，用于 PDF 转图片
    "Pillow>=10.0.0",
]

# PaddleOCR 3.x 依赖
PADDLEOCR_PACKAGE = "paddleocr>=3.0"

# PaddlePaddle 版本配置
PADDLE_CPU = "paddlepaddle>=3.0"
PADDLE_GPU = "paddlepaddle-gpu==3.0.0"
PADDLE_GPU_INDEX = "https://www.paddlepaddle.org.cn/packages/stable/cu126/"


def setup_encoding():
    """设置输出编码"""
    import io
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def check_uv() -> bool:
    """检查 uv 是否已安装"""
    try:
        subprocess.run(["uv", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_uv():
    """安装 uv"""
    print("📦 安装 uv (Python 快速包管理器)...")
    
    if sys.platform == "win32":
        # Windows 使用 PowerShell 安装
        cmd = [
            "powershell", "-ExecutionPolicy", "ByPass", "-c",
            "irm https://astral.sh/uv/install.ps1 | iex"
        ]
    else:
        # macOS/Linux 使用 curl
        cmd = ["sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ uv 安装失败: {result.stderr}")
            print("请手动安装 uv: https://github.com/astral-sh/uv")
            sys.exit(1)
        print("✅ uv 安装成功")
    except Exception as e:
        print(f"❌ uv 安装出错: {e}")
        print("请手动安装 uv: https://github.com/astral-sh/uv")
        sys.exit(1)


def create_venv(skill_dir: Path) -> Path:
    """创建虚拟环境"""
    venv_path = skill_dir / VENV_NAME

    if venv_path.exists():
        print(f"📁 虚拟环境已存在: {venv_path}")
        return venv_path

    print(f"📁 创建虚拟环境: {venv_path}")
    print("🐍 使用 Python 3.12 (PaddlePaddle GPU 支持)")

    try:
        subprocess.run(
            ["uv", "venv", "-p", "python3.12", str(venv_path)],
            capture_output=True,
            check=True
        )
        print("✅ 虚拟环境创建成功")
        return venv_path
    except subprocess.CalledProcessError as e:
        print(f"⚠️ 使用 Python 3.12 失败，尝试默认版本: {e}")
        try:
            subprocess.run(
                ["uv", "venv", str(venv_path)],
                capture_output=True,
                check=True
            )
            print("✅ 虚拟环境创建成功（默认版本）")
            return venv_path
        except subprocess.CalledProcessError as e2:
            print(f"❌ 创建虚拟环境失败: {e2}")
            sys.exit(1)


def get_venv_python(venv_path: Path) -> Path:
    """获取虚拟环境中的 Python 路径"""
    if sys.platform == "win32":
        return venv_path / "Scripts" / "python.exe"
    else:
        return venv_path / "bin" / "python"


def check_cuda() -> bool:
    """检查是否有可用的 CUDA"""
    try:
        result = subprocess.run(
            ["nvcc", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            # 解析 CUDA 版本
            for line in result.stdout.split('\n'):
                if 'release' in line:
                    print(f"   检测到 CUDA: {line.strip()}")
                    return True
        return False
    except FileNotFoundError:
        return False


def install_packages(venv_path: Path, use_gpu: bool = False):
    """安装依赖包"""
    print("📦 安装基础依赖包...")

    python_exe = get_venv_python(venv_path)

    # 1. 安装基础依赖
    try:
        cmd = ["uv", "pip", "install", "--python", str(python_exe)] + REQUIRED_PACKAGES
        subprocess.run(cmd, check=True)
        print("✅ 基础依赖安装成功")
    except subprocess.CalledProcessError as e:
        print(f"❌ 安装基础依赖失败: {e}")
        sys.exit(1)

    # 2. 安装 PaddlePaddle
    print("📦 安装 PaddlePaddle...")
    if use_gpu:
        print("⚡ 使用 GPU 版本 (CUDA 12.6)")
        try:
            cmd = [
                "uv", "pip", "install", "--python", str(python_exe),
                PADDLE_GPU, "-i", PADDLE_GPU_INDEX
            ]
            subprocess.run(cmd, check=True)
            print("✅ PaddlePaddle GPU 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ GPU 版本安装失败，尝试 CPU 版本: {e}")
            try:
                cmd = ["uv", "pip", "install", "--python", str(python_exe), PADDLE_CPU]
                subprocess.run(cmd, check=True)
                print("✅ PaddlePaddle CPU 安装成功")
            except subprocess.CalledProcessError as e2:
                print(f"❌ PaddlePaddle 安装失败: {e2}")
                sys.exit(1)
    else:
        print("💻 使用 CPU 版本")
        try:
            cmd = ["uv", "pip", "install", "--python", str(python_exe), PADDLE_CPU]
            subprocess.run(cmd, check=True)
            print("✅ PaddlePaddle CPU 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ PaddlePaddle 安装失败: {e}")
            sys.exit(1)

    # 3. 安装 PaddleOCR 3.x
    print("📦 安装 PaddleOCR 3.x...")
    try:
        cmd = ["uv", "pip", "install", "--python", str(python_exe), PADDLEOCR_PACKAGE]
        subprocess.run(cmd, check=True)
        print("✅ PaddleOCR 安装成功")
    except subprocess.CalledProcessError as e:
        print(f"❌ PaddleOCR 安装失败: {e}")
        sys.exit(1)


def download_ocr_models(venv_path: Path, use_gpu: bool = False):
    """预下载 OCR 模型 (PaddleOCR 3.x)"""
    print("📥 预下载 OCR 模型（首次使用需要，约 200MB）...")
    print("   提示: PaddleOCR 3.x 模型将在首次使用时自动下载")
    print("   跳过预下载，首次运行时会自动获取...")
    print("✅ 模型配置完成 (将在首次使用时自动下载)")


def create_activation_scripts(skill_dir: Path, venv_path: Path):
    """创建激活脚本"""
    
    # Windows PowerShell 脚本
    ps_script = f'''# Quick Book Mastery Skill 激活脚本
$venvPath = "{venv_path}"

if (Test-Path "$venvPath\\Scripts\\Activate.ps1") {{
    & "$venvPath\\Scripts\\Activate.ps1"
    Write-Host "✅ Skill 环境已激活" -ForegroundColor Green
}} else {{
    Write-Host "❌ 虚拟环境不存在，请先运行 install.py" -ForegroundColor Red
}}
'''
    
    # Windows CMD 脚本
    cmd_script = f'''@echo off
call "{venv_path}\\Scripts\\activate.bat"
if %errorlevel% == 0 (
    echo ✅ Skill 环境已激活
) else (
    echo ❌ 虚拟环境不存在，请先运行 install.py
)
'''
    
    # Bash 脚本 (macOS/Linux)
    bash_script = f'''#!/bin/bash
VENV_PATH="{venv_path}"

if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"
    echo "✅ Skill 环境已激活"
else
    echo "❌ 虚拟环境不存在，请先运行 install.py"
fi
'''
    
    scripts_dir = skill_dir / "scripts"
    
    with open(scripts_dir / "activate.ps1", "w", encoding="utf-8") as f:
        f.write(ps_script)
    
    with open(scripts_dir / "activate.bat", "w", encoding="utf-8") as f:
        f.write(cmd_script)
    
    with open(scripts_dir / "activate.sh", "w", encoding="utf-8") as f:
        f.write(bash_script)
    
    print("✅ 激活脚本已创建")


def verify_installation(venv_path: Path, use_gpu: bool = False) -> bool:
    """验证安装"""
    print("🔍 验证安装...")

    python_exe = get_venv_python(venv_path)
    all_ok = True

    # 1. 检查基础依赖
    checks = [
        ("pdfplumber", "import pdfplumber; print('✅ pdfplumber')"),
        ("PyMuPDF", "import fitz; print('✅ PyMuPDF (fitz)')"),
        ("Pillow", "from PIL import Image; print('✅ Pillow')"),
    ]

    for name, code in checks:
        try:
            result = subprocess.run(
                [str(python_exe), "-c", code],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                print(f"  {result.stdout.strip()}")
            else:
                print(f"  ❌ {name} 导入失败")
                all_ok = False
        except Exception as e:
            print(f"  ❌ {name} 检查失败: {e}")
            all_ok = False

    # 2. 检查 PaddlePaddle 版本和 GPU 支持
    print("  📦 PaddlePaddle 信息:")
    try:
        paddle_check = f"""
import paddle
print(f"   版本: {{paddle.__version__}}")
print(f"   CUDA 可用: {{paddle.is_compiled_with_cuda()}}")
if paddle.is_compiled_with_cuda():
    print(f"   CUDA 版本: {{paddle.version.cuda()}}")
    print(f"   cuDNN 版本: {{paddle.version.cudnn()}}")
"""
        result = subprocess.run(
            [str(python_exe), "-c", paddle_check],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print(f"   ⚠️ 无法获取 PaddlePaddle 信息: {result.stderr}")
    except Exception as e:
        print(f"   ⚠️ PaddlePaddle 检查失败: {e}")

    # 3. 检查 PaddleOCR
    print("  📦 PaddleOCR 信息:")
    try:
        ocr_check = """
from paddleocr import PaddleOCR
import paddleocr
print(f"   版本: {paddleocr.__version__}")
print("   ✅ PaddleOCR 导入成功")
"""
        result = subprocess.run(
            [str(python_exe), "-c", ocr_check],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print(f"   ❌ PaddleOCR 检查失败: {result.stderr}")
            all_ok = False
    except Exception as e:
        print(f"   ❌ PaddleOCR 检查失败: {e}")
        all_ok = False

    return all_ok


def create_config(skill_dir: Path, venv_path: Path):
    """创建配置文件"""
    config = {
        "venv_path": str(venv_path),
        "python_path": str(get_venv_python(venv_path)),
        "installed_at": str(__import__('datetime').datetime.now()),
        "version": "1.0.0"
    }
    
    import json
    config_path = skill_dir / ".skill_config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ 配置文件已创建: {config_path}")


def main():
    setup_encoding()
    
    print("=" * 60)
    print("📚 Quick Book Mastery Skill 安装程序")
    print("=" * 60)
    print()
    
    # 获取 skill 目录
    script_dir = Path(__file__).parent.resolve()
    skill_dir = script_dir.parent
    
    print(f"📁 Skill 目录: {skill_dir}")
    print()
    
    # 1. 检查 uv
    if not check_uv():
        print("⚠️  未检测到 uv，正在安装...")
        install_uv()
        # 重新检查
        if not check_uv():
            print("❌ uv 安装后仍未检测到，请手动安装并添加到 PATH")
            sys.exit(1)
    else:
        print("✅ uv 已安装")
    
    # 2. 询问是否使用 GPU
    use_gpu = False
    if sys.platform != "darwin":  # macOS 不支持 CUDA
        response = input("\n是否使用 GPU 版本 (CUDA)? [y/N]: ").strip().lower()
        use_gpu = response in ('y', 'yes')
    
    # 3. 创建虚拟环境
    print()
    venv_path = create_venv(skill_dir)
    
    # 4. 安装依赖
    print()
    install_packages(venv_path, use_gpu)
    
    # 5. 下载 OCR 模型
    print()
    download_ocr_models(venv_path)
    
    # 6. 创建激活脚本
    print()
    create_activation_scripts(skill_dir, venv_path)
    
    # 7. 验证安装
    print()
    if verify_installation(venv_path, use_gpu):
        print("\n✅ 所有检查通过！")
    else:
        print("\n⚠️  部分检查未通过，但基本功能应该可用")
    
    # 8. 创建配置文件
    print()
    create_config(skill_dir, venv_path)
    
    # 完成
    print()
    print("=" * 60)
    print("🎉 安装完成！")
    print("=" * 60)
    print()
    print("使用说明:")
    print("  1. 激活环境:")
    if sys.platform == "win32":
        print(f"     powershell -ExecutionPolicy ByPass -File \"{skill_dir / 'scripts' / 'activate.ps1'}\"")
    else:
        print(f"     source {skill_dir / 'scripts' / 'activate.sh'}")
    print()
    print("  2. 使用 OCR 功能:")
    print(f"     python {skill_dir / 'scripts' / 'pdf_reader.py'} <pdf> --ocr")
    print()
    print("  3. 或者直接在命令行使用 (会自动使用虚拟环境):")
    print(f"     python {skill_dir / 'scripts' / 'pdf_reader.py'} <pdf> --overview")
    print()


if __name__ == "__main__":
    main()
