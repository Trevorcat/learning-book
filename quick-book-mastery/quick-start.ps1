# Quick Book Mastery Skill - 快速启动脚本
# 支持 OCR 的 PDF 阅读器启动器

$SkillDir = $PSScriptRoot
$VenvPath = Join-Path $SkillDir ".venv"
$PythonExe = Join-Path $VenvPath "Scripts\python.exe"
$ReaderScript = Join-Path $SkillDir "scripts\pdf_reader.py"

function Show-Header {
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host "  Quick Book Mastery Skill - 快速启动" -ForegroundColor Cyan
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Test-VirtualEnvironment {
    if (-not (Test-Path $PythonExe)) {
        Write-Host "[首次使用] 正在安装依赖..." -ForegroundColor Yellow
        Write-Host ""
        
        $InstallScript = Join-Path $SkillDir "scripts\install.py"
        & python $InstallScript
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "安装失败，请检查错误信息" -ForegroundColor Red
            Read-Host "按 Enter 键退出"
            exit 1
        }
    }
}

function Get-PdfPath {
    Write-Host "请输入 PDF 文件路径（可拖放文件）:" -ForegroundColor Green
    $path = Read-Host "PDF 路径"
    
    # 去除引号
    $path = $path.Trim('"', "'")
    
    if (-not (Test-Path $path)) {
        Write-Host "错误: 文件不存在" -ForegroundColor Red
        Read-Host "按 Enter 键退出"
        exit 1
    }
    
    return $path
}

function Show-Menu {
    Write-Host "请选择操作:" -ForegroundColor Green
    Write-Host ""
    Write-Host "  1. 获取 PDF 概览" -ForegroundColor White
    Write-Host "  2. 提取目录" -ForegroundColor White
    Write-Host "  3. 提取目录 + OCR（扫描版）" -ForegroundColor Yellow
    Write-Host "  4. 读取指定页" -ForegroundColor White
    Write-Host "  5. 搜索关键词" -ForegroundColor White
    Write-Host "  6. 生成大纲" -ForegroundColor White
    Write-Host "  7. 退出" -ForegroundColor Gray
    Write-Host ""
}

# 主程序
Show-Header
Test-VirtualEnvironment

$running = $true
while ($running) {
    Show-Menu
    $choice = Read-Host "输入选项 (1-7)"
    
    switch ($choice) {
        "1" {
            $pdf = Get-PdfPath
            Write-Host "`n正在处理..." -ForegroundColor Cyan
            & $PythonExe $ReaderScript $pdf --overview
        }
        "2" {
            $pdf = Get-PdfPath
            Write-Host "`n正在处理..." -ForegroundColor Cyan
            & $PythonExe $ReaderScript $pdf --toc
        }
        "3" {
            $pdf = Get-PdfPath
            Write-Host "`n正在处理（OCR 模式，请稍候）..." -ForegroundColor Yellow
            & $PythonExe $ReaderScript $pdf --toc --ocr
        }
        "4" {
            $pdf = Get-PdfPath
            $pages = Read-Host "输入页码范围 (如: 10-20)"
            Write-Host "`n正在处理..." -ForegroundColor Cyan
            & $PythonExe $ReaderScript $pdf --pages $pages
        }
        "5" {
            $pdf = Get-PdfPath
            $keyword = Read-Host "输入搜索关键词"
            Write-Host "`n正在搜索..." -ForegroundColor Cyan
            & $PythonExe $ReaderScript $pdf --search $keyword
        }
        "6" {
            $pdf = Get-PdfPath
            Write-Host "`n正在生成大纲..." -ForegroundColor Cyan
            & $PythonExe $ReaderScript $pdf --outline
        }
        "7" {
            $running = $false
            continue
        }
        default {
            Write-Host "无效选项" -ForegroundColor Red
        }
    }
    
    if ($running) {
        Write-Host "`n================================================" -ForegroundColor Cyan
        Read-Host "按 Enter 键继续"
        Clear-Host
        Show-Header
    }
}

Write-Host "再见！" -ForegroundColor Green
