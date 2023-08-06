from setuptools import setup, find_packages


setup(
    author='Shakhzod Dadabaev Urazalievich',
    description='Optimization for Geant4 application at gitlab.cern: spacal-simulation',
    name='spacopt',
    version='0.1.0',
    packages=find_packages(include=['spacopt', 'spacopt.*']),
    install_requires=['pandas>=1.4',
                      'hyperactive>=4.1.1', 
                      'matplotlib>=3.5', 
                      'numpy>=1.22', 
                      'root_numpy>=4.8.0'],
    python_requires='>=3.8',
)