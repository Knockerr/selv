# build.ps1
$ErrorActionPreference = "Stop"
Set-Location backend
.venv\Scripts\python.exe -m PyInstaller main.spec --distpath ../src-tauri/binaries
Set-Location ..
npm run tauri build
