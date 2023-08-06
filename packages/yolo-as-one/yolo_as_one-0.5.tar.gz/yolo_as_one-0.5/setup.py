from setuptools import setup, find_packages

setup(
    name='yolo_as_one',
    version='0.5',
    license='MIT',
    author="Bramwel Ochieng",
    author_email='lol@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/ochi96/yolo_as_one',
    keywords='yolo installation inferencing',
    install_requires=[
        'scikit-learn',
        'numpy',
        'torch>=1.7.0',
        'opencv_python',
        'loguru',
        'scikit-image',
        'tqdm',
        'torchvision',
        'Pillow',
        'thop',
        'ninja',
        'tabulate',
        'tensorboard',
        'PyYAML>=5.3.1',
        'pandas>=1.1.4',
        'seaborn>=0.11.0',
        'thop',
        'requests>=2.23.0',
        'matplotlib>=3.2.2',
      ],

    scripts=[
        './src/installation_scripts/yolor.sh',
        './src/installation_scripts/yolox.sh',
        './src/installation_scripts/yolov5.sh',
        './src/installation_scripts/yolor.bat',
        './src/installation_scripts/yolox.bat',
        './src/installation_scripts/yolov5.bat',
    ]
)