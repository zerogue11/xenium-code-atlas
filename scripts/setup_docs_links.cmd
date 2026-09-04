@echo off
rem 重建 mkdocs 站点所需的 NTFS 目录联接（fresh clone 后运行一次）
rem 用法：在仓库根目录运行  cmd /c scripts\setup_docs_links.cmd
setlocal
cd /d "%~dp0.."

if not exist "docs\01_资料库" mklink /J "docs\01_资料库" "01_资料库"
if not exist "docs\02_工作流开发" mklink /J "docs\02_工作流开发" "02_工作流开发"

echo 完成：docs 下联接已就绪（若未显示创建信息则此前已存在）。
endlocal
