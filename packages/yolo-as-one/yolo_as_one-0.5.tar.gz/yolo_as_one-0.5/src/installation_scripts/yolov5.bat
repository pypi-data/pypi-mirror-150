git clone https://github.com/ultralytics/yolov5.git

cd yolov5

python -m venv winvenv


CALL winvenv/Scripts/activate.bat

python -m pip install --upgrade pip

pip install -r requirements.txt

pip install pycocotools-windows

pip install gdown

gdown https://drive.google.com/uc?id=1drHpDPVu-GqIo9nFVatys3uHoGjNn-7D


CALL winvenv/Scripts/deactivate.bat

cd ..

