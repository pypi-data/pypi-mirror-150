
git clone https://github.com/Megvii-BaseDetection/YOLOX.git

cd YOLOX

python3 -m venv linvenv

. linvenv/bin/activate

pip3 install --upgrade pip

pip3 install -r requirements.txt

python3 setup.py install

mkdir -p weights

wget https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_s.pth -O ./weights/yolox_s.pth


