set -e
cd backend
export BINARY_NAME="selv-backend-x86_64-unknown-linux-gnu"
.venv/bin/python -m PyInstaller main.spec --distpath ../src-tauri/binaries
cd ..