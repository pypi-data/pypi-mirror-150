

git clone https://github.com/ochi96/yolox.git

cd yolox

python3 setup.py install

mkdir -p weights

wget https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_s.pth -O ./weights/yolox_s.pth

