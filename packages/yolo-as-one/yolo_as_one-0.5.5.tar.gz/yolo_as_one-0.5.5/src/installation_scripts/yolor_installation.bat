
git clone https://github.com/WongKinYiu/yolor.git

cd yolor

python -m venv winvenv

CALL winvenv/Scripts/activate.bat

python -m pip install --upgrade pip

pip install -r requirements.txt

pip install pycocotools-windows

git clone https://github.com/fbcotter/pytorch_wavelets

cd pytorch_wavelets

pip install .

cd ..

pip install gdown

mkdir weights

gdown https://drive.google.com/uc?id=13lZlcjo-9uqU0MnV1lfG4YqPot4twqUi -O ./weights/yolor_p6.pt

CALL winvenv/Scripts/deactivate.bat

cd ..

