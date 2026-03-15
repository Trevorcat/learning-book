#!/usr/bin/env python3
"""
虚拟环境管理工具

自动检测和管理 Quick Book Mastery Skill 的虚拟环境
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple


class VenvManager:
    """虚拟环境管理器"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent.resolve()
        self.skill_dir = self.script_dir.parent
        self.config_path = self.skill_dir / ".skill_config.json"
        self.default_venv_path = self.skill_dir / ".venv"
    
    def find_venv(self) -> Optional[Path]:
        """查找虚拟环境"""
        # 1. 从配置文件读取
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    venv_path = Path(config.get("venv_path", ""))
                    if venv_path.exists():
                        return venv_path
            except:
                pass
        
        # 2. 检查默认位置
        if self.default_venv_path.exists():
            return self.default_venv_path
        
        # 3. 检查常见位置
        for venv_name in [".venv", "venv", "env"]:
            path = self.skill_dir / venv_name
            if path.exists():
                return path
        
        return None
    
    def get_python_executable(self, venv_path: Path) -> Path:
        """获取虚拟环境的 Python 可执行文件"""
        if sys.platform == "win32":
            return venv_path / "Scripts" / "python.exe"
        else:
            return venv_path / "bin" / "python"
    
    def is_venv_active(self) -> bool:
        """检查当前是否在虚拟环境中"""
        return hasattr(sys, 'real_prefix') or (
            hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
        )
    
    def run_in_venv(self, script_name: str, args: list) -> int:
        """
        在虚拟环境中运行脚本
        
        Args:
            script_name: 脚本文件名（在 scripts 目录中）
            args: 传递给脚本的参数
        
        Returns:
            返回码
        """
        venv_path = self.find_venv()
        
        if not venv_path:
            print("❌ 未找到虚拟环境")
            print(f"   请先运行安装脚本: python {self.script_dir / 'install.py'}")
            return 1
        
        python_exe = self.get_python_executable(venv_path)
        script_path = self.script_dir / script_name
        
        if not python_exe.exists():
            print(f"❌ Python 可执行文件不存在: {python_exe}")
            return 1
        
        # 构建命令
        cmd = [str(python_exe), str(script_path)] + args
        
        # 设置环境变量
        env = os.environ.copy()
        env["VIRTUAL_ENV"] = str(venv_path)
        
        if sys.platform == "win32":
            env["PATH"] = str(venv_path / "Scripts") + os.pathsep + env.get("PATH", "")
        else:
            env["PATH"] = str(venv_path / "bin") + os.pathsep + env.get("PATH", "")
        
        try:
            result = subprocess.run(cmd, env=env)
            return result.returncode
        except Exception as e:
            print(f"❌ 运行失败: {e}")
            return 1
    
    def ensure_dependencies(self) -> bool:
        """确保依赖已安装"""
        venv_path = self.find_venv()
        if not venv_path:
            return False
        
        python_exe = self.get_python_executable(venv_path)
        
        # 检查关键依赖
        check_code = '''
try:
    import pdfplumber
    import fitz
    from paddleocr import PaddleOCR
    print("OK")
except ImportError as e:
    print(f"MISSING: {e}")
'''
        try:
            result = subprocess.run(
                [str(python_exe), "-c", check_code],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0 and "OK" in result.stdout
        except:
            return False


def setup_encoding():
    """设置输出编码"""
    import io
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def main():
    """命令行工具"""
    setup_encoding()
    
    import argparse
    parser = argparse.ArgumentParser(description="Skill 虚拟环境管理")
    parser.add_argument("command", choices=["status", "run", "check"],
                       help="命令: status(查看状态), run(运行脚本), check(检查依赖)")
    parser.add_argument("--script", "-s", help="要运行的脚本名（用于 run 命令）")
    parser.add_argument("args", nargs="*", help="传递给脚本的参数")
    
    args = parser.parse_args()
    
    manager = VenvManager()
    
    if args.command == "status":
        venv = manager.find_venv()
        if venv:
            print(f"✅ 找到虚拟环境: {venv}")
            print(f"   Python: {manager.get_python_executable(venv)}")
            print(f"   当前激活: {'是' if manager.is_venv_active() else '否'}")
        else:
            print("❌ 未找到虚拟环境")
            print(f"   请运行: python {manager.script_dir / 'install.py'}")
    
    elif args.command == "check":
        if manager.ensure_dependencies():
            print("✅ 所有依赖已安装")
        else:
            print("❌ 依赖检查失败")
            print("   请运行安装脚本")
    
    elif args.command == "run":
        if not args.script:
            print("❌ 请指定脚本名: --script pdf_reader.py")
            sys.exit(1)
        
        code = manager.run_in_venv(args.script, args.args or [])
        sys.exit(code)


if __name__ == "__main__":
    main()
