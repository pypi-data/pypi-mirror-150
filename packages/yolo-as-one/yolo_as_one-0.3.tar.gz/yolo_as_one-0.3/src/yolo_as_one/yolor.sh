

git clone https://github.com/WongKinYiu/yolor.git

cd yolor

python3 -m venv linvenv

. linvenv/bin/activate

pip3 install --upgrade pip

pip3 install -r requirements.txt

pip3 install pycocotools

git clone https://github.com/fbcotter/pytorch_wavelets

cd pytorch_wavelets

pip install .

cd ..

pip3 install gdown

mkdir -p weights

gdown https://drive.google.com/uc?id=13lZlcjo-9uqU0MnV1lfG4YqPot4twqUi -O ./weights/yolor_p6.pt



