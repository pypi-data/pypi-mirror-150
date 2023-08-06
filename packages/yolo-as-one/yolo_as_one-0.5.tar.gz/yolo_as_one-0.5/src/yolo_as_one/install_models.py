
import argparse
from subprocess import call
from sys import platform

model_names = ['yolox', 'yolor', 'yolov5']

def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('--model_name', default='None')
    return parse.parse_args()


def install_models(model_name):
    if model_name in model_names:
        if platform == "linux" or platform == "linux2":
            call(f"{model_name}.sh", shell=True)
        elif platform == "win32":
            call(f"{model_name}.bat", shell=True)
        else:
            print('Operating Sytem unsupported')
    else:
        print('model not currently available')
    pass

def run_models(model_name):

    
    pass

if __name__=='__main__':
    args = parse_args()
    install_models(args.model_name)
