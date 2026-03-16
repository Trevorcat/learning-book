# Quick Book Mastery Skill 激活脚本
$venvPath = "C:\Users\chenkejie\.claude\skills\learning-book\quick-book-mastery\.venv"

if (Test-Path "$venvPath\Scripts\Activate.ps1") {
    & "$venvPath\Scripts\Activate.ps1"
    Write-Host "✅ Skill 环境已激活" -ForegroundColor Green
} else {
    Write-Host "❌ 虚拟环境不存在，请先运行 install.py" -ForegroundColor Red
}
