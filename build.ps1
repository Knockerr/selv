# build.ps1
Set-Location backend
.venv\Scripts\activate
pyinstaller --onefile  --noconsole --name mcpanel-backend-x86_64-pc-windows-msvc --distpath ../src-tauri/binaries main.py
deactivate
Set-Location ..
npm run tauri build
