from setuptools import setup, find_packages

setup(
    name='aixlab.cn',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'opencv-contrib-python', 
        'Flask' ,
        'scipy',
        'matplotlib==3.2.2' ,
        'flask-cors',
        'torch==1.8.0', 
        'torchvision==0.10.0',
        'requests'
    ],
    author='Xu Ziyi',
    author_email='759946140@qq.com',
    description='Support for aixlab.cn',
    url='https://github.com/xuzycuan/aixlab.cn',
    license='MIT'
)
