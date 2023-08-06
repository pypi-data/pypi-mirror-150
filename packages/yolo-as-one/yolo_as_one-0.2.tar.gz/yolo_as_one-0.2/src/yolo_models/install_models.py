
import argparse
from subprocess import call

model_names = ['yolox', 'yolor', 'yolov5']

def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('--model_name', default='None')
    return parse.parse_args()


def install_models(model_name):
    if model_name in model_names:
        call(f"./{model_name}.sh", shell=True)
    else:
        print('model not currently available')
    pass

if __name__=='__main__':
    args = parse_args()
    install_models(args.model_name)
