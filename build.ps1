# build.ps1
Set-Location backend
.venv\Scripts\activate
pyinstaller --onefile --name mcpanel-backend --distpath ../src-tauri/binaries main.py
deactivate
Set-Location ..
npm run tauri build
