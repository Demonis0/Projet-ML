@echo off

cd stable-diffusion-webui
start cmd /k "call webui-user.bat"

cd ..
cd MLAPI\.venv\Scripts
call activate.bat
cd ..
cd ..
pip install -r requirements.txt
start cmd /k "python -m flask --app main_mlapi run"


cd..
cd MLFRONT
npm install
start cmd /k "npm run serve"

