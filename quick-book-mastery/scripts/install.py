#!/usr/bin/env python3
"""
Quick Book Mastery Skill 安装脚本

自动完成：
1. 检查并安装 uv（如果未安装）
2. 创建虚拟环境
3. 安装所有依赖（包括 PaddleOCR）
4. 下载 OCR 模型
5. 验证安装

使用方法:
    python install.py

要求:
    - Python 3.8+
    - 网络连接（下载模型和依赖）
"""

import os
import subprocess
import sys
from pathlib import Path

# 配置
VENV_NAME = ".venv"
REQUIRED_PACKAGES = [
    "pdfplumber>=0.10.0",
    "paddlepaddle>=2.5.0",  # CPU 版本
    "paddleocr>=2.7.0",
    "pymupdf>=1.23.0",  # fitz，用于 PDF 转图片
    "Pillow>=10.0.0",
]

# 可选 GPU 版本（如果有 CUDA）
GPU_PACKAGES = [
    "paddlepaddle-gpu>=2.5.0",
]


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
    
    try:
        subprocess.run(
            ["uv", "venv", str(venv_path)],
            capture_output=True,
            check=True
        )
        print("✅ 虚拟环境创建成功")
        return venv_path
    except subprocess.CalledProcessError as e:
        print(f"❌ 创建虚拟环境失败: {e}")
        sys.exit(1)


def get_venv_python(venv_path: Path) -> Path:
    """获取虚拟环境中的 Python 路径"""
    if sys.platform == "win32":
        return venv_path / "Scripts" / "python.exe"
    else:
        return venv_path / "bin" / "python"


def install_packages(venv_path: Path, use_gpu: bool = False):
    """安装依赖包"""
    print("📦 安装依赖包...")
    
    packages = REQUIRED_PACKAGES.copy()
    
    # 如果使用 GPU，替换 paddlepaddle 为 paddlepaddle-gpu
    if use_gpu:
        packages = [p for p in packages if not p.startswith("paddlepaddle>")]
        packages.extend(GPU_PACKAGES)
        print("⚡ 使用 GPU 版本 (CUDA)")
    
    try:
        # 使用 uv pip install
        cmd = ["uv", "pip", "install", "--python", str(get_venv_python(venv_path))] + packages
        subprocess.run(cmd, check=True)
        print("✅ 依赖包安装成功")
    except subprocess.CalledProcessError as e:
        print(f"❌ 安装依赖失败: {e}")
        sys.exit(1)


def download_ocr_models(venv_path: Path):
    """预下载 OCR 模型"""
    print("📥 预下载 OCR 模型（首次使用需要）...")
    
    python_exe = get_venv_python(venv_path)
    
    # 创建临时脚本来下载模型
    script = '''
from paddleocr import PaddleOCR
import os

# 设置模型下载路径
os.environ['PADDLE_OCR_HOME'] = os.path.expanduser('~/.paddleocr')

print("正在下载中文 OCR 模型...")
ocr = PaddleOCR(
    use_angle_cls=True,
    lang='ch',
    show_log=False,
    use_gpu=False
)
print("✅ 中文模型下载完成")

print("正在下载英文 OCR 模型...")
ocr_en = PaddleOCR(
    use_angle_cls=True,
    lang='en',
    show_log=False,
    use_gpu=False
)
print("✅ 英文模型下载完成")
'''
    
    try:
        result = subprocess.run(
            [str(python_exe), "-c", script],
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )
        
        if result.returncode == 0:
            print("✅ OCR 模型准备完成")
        else:
            print(f"⚠️  模型下载可能未完成，将在首次使用时自动下载")
            print(f"   错误: {result.stderr[:200]}")
    except subprocess.TimeoutExpired:
        print("⚠️  模型下载超时，将在首次使用时自动下载")
    except Exception as e:
        print(f"⚠️  模型预下载失败: {e}")
        print("   将在首次使用时自动下载")


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


def verify_installation(venv_path: Path) -> bool:
    """验证安装"""
    print("🔍 验证安装...")
    
    python_exe = get_venv_python(venv_path)
    
    checks = [
        ("pdfplumber", "import pdfplumber; print('✅ pdfplumber')"),
        ("PyMuPDF", "import fitz; print('✅ PyMuPDF (fitz)')"),
        ("PaddleOCR", "from paddleocr import PaddleOCR; print('✅ PaddleOCR')"),
        ("Pillow", "from PIL import Image; print('✅ Pillow')"),
    ]
    
    all_ok = True
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
    if verify_installation(venv_path):
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
