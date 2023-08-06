from sys import platform

pycoco = 'pycocotools' if platform=='win32' else 'pycocotools-windows'

print(type(pycoco))
