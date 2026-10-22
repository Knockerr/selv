# build.ps1
$ErrorActionPreference = "Stop"
Set-Location backend
$env:BINARY_NAME="selv-backend-x86_64-pc-windows-msvc.exe";
.venv\Scripts\python.exe -m PyInstaller main.spec --distpath ../src-tauri/binaries
Set-Location ..