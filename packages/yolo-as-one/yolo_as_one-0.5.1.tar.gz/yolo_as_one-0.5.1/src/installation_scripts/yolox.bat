git clone https://github.com/Megvii-BaseDetection/YOLOX.git

cd YOLOX

python -m venv winvenv


CALL winvenv/Scripts/activate.bat

python -m pip install --upgrade pip

cd ..

copy /Y "requirements.txt" "YOLOX/requirements.txt"

cd YOLOX

pip install -r requirements.txt

python setup.py install

pip install gdown

mkdir weights

gdown https://drive.google.com/uc?id=1q_f0fG0MnQ0JVEFkVoIXDZ2_KZ2oAcf8 -O ./weights/yolox_s.pth

CALL winvenv/Scripts/deactivate.bat

cd ..


REM WEBCAM INFERENCING
REM python tools/demo.py webcam -f exps/default/yolox_s.py -c ./weights/yolox_s.pth  --conf 0.3 --nms 0.65 --tsize 640 --save_result --device cpu

REM VIDEO INFERENCING
REM python tools/demo.py video -f exps/default/yolox_s.py -c ./weights/yolox_s.pth --path assets/lol.mp4 --conf 0.3 --nms 0.65 --tsize 640 --save_result --device cpu




