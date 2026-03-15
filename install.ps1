#!/usr/bin/env pwsh
# Quick Book Mastery Skill - Windows 一键安装脚本
# 安装地址: https://github.com/Trevorcat/learning-book

$ErrorActionPreference = "Stop"

# 配置
$RepoUrl = "https://github.com/Trevorcat/learning-book.git"
$SkillName = "quick-book-mastery"
$InstallDir = "$env:USERPROFILE\.agents\skills\$SkillName"

function Write-Header {
    Write-Host ""
    Write-Host "===============================================" -ForegroundColor Cyan
    Write-Host "  Quick Book Mastery Skill - 一键安装" -ForegroundColor Cyan
    Write-Host "===============================================" -ForegroundColor Cyan
    Write-Host ""
}

function Test-Git {
    try {
        $null = Get-Command git -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

function Install-Git {
    Write-Host "📦 Git 未安装，正在下载安装..." -ForegroundColor Yellow
    
    # 下载 Git for Windows
    $gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
    $gitInstaller = "$env:TEMP\git-installer.exe"
    
    try {
        Invoke-WebRequest -Uri $gitUrl -OutFile $gitInstaller -UseBasicParsing
        Write-Host "🚀 启动 Git 安装程序，请按提示完成安装..." -ForegroundColor Green
        Start-Process -FilePath $gitInstaller -Wait
        
        # 刷新环境变量
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
        
        Write-Host "✅ Git 安装完成，请重新运行此脚本" -ForegroundColor Green
        exit 0
    } catch {
        Write-Host "❌ Git 下载/安装失败: $_" -ForegroundColor Red
        Write-Host "请手动下载安装: https://git-scm.com/download/win" -ForegroundColor Yellow
        exit 1
    }
}

function Install-Skill {
    Write-Header
    
    # 检查 Git
    if (-not (Test-Git)) {
        Install-Git
    }
    
    Write-Host "✅ Git 已安装"
    Write-Host ""
    
    # 创建安装目录
    $parentDir = Split-Path $InstallDir -Parent
    if (-not (Test-Path $parentDir)) {
        New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
    }
    
    # 如果已存在，先备份
    if (Test-Path $InstallDir) {
        $backupName = "$SkillName-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        Write-Host "📁 检测到已安装，备份到: $backupName" -ForegroundColor Yellow
        Rename-Item $InstallDir "$parentDir\$backupName"
    }
    
    # 克隆仓库
    Write-Host "📥 正在下载 Skill..." -ForegroundColor Cyan
    try {
        git clone --depth 1 $RepoUrl $InstallDir
        Write-Host "✅ 下载完成" -ForegroundColor Green
    } catch {
        Write-Host "❌ 下载失败: $_" -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    Write-Host "📦 正在安装依赖（这可能需要几分钟）..." -ForegroundColor Cyan
    
    # 运行安装脚本
    $installScript = Join-Path $InstallDir "quick-book-mastery\scripts\install.py"
    if (Test-Path $installScript) {
        Set-Location (Split-Path $installScript -Parent)
        python install.py
    } else {
        Write-Host "⚠️ 安装脚本不存在，尝试手动安装依赖..." -ForegroundColor Yellow
        # 手动安装
        $venvDir = Join-Path $InstallDir "quick-book-mastery\.venv"
        
        # 检查 uv
        try {
            $null = Get-Command uv -ErrorAction Stop
        } catch {
            Write-Host "📦 安装 uv..." -ForegroundColor Cyan
            irm https://astral.sh/uv/install.ps1 | iex
        }
        
        # 创建虚拟环境
        Set-Location (Join-Path $InstallDir "quick-book-mastery")
        uv venv .venv
        
        # 安装依赖
        $venvPython = Join-Path $venvDir "Scripts\python.exe"
        uv pip install --python $venvPython pdfplumber paddlepaddle paddleocr pymupdf Pillow
    }
    
    Write-Host ""
    Write-Host "===============================================" -ForegroundColor Green
    Write-Host "  ✅ 安装完成！" -ForegroundColor Green
    Write-Host "===============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "使用方法:" -ForegroundColor Cyan
    Write-Host "  1. 快速启动:"
    Write-Host "     $InstallDir\quick-book-mastery\quick-start.ps1" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  2. 命令行使用:"
    Write-Host "     cd $InstallDir\quick-book-mastery" -ForegroundColor Yellow
    Write-Host "     .venv\Scripts\python.exe scripts\pdf_reader.py <pdf> --overview" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  3. 在 Kimi Code CLI 中使用:"
    Write-Host "     直接说: '帮我学习这本书'" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📖 文档: https://github.com/Trevorcat/learning-book" -ForegroundColor Gray
    Write-Host ""
}

# 运行安装
Install-Skill
