from setuptools import find_packages, setup

setup(
    name='model_creator_bird_sing_v2',
    packages=['model_creator/'],
    version='0.1.8',
    description='Autoencoder singing',
    author='VIRGAUX Pierre',
    license='MIT',
    install_requires=['tensorflow==2.3.1','mutagen','pydub','ray', 'librosa', 'keras-tuner', 'wandb'],
)