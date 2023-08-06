from setuptools import setup, find_packages

setup(
    name='PowDeRUL',
    version='1.0.3',
    description='Python package for calculating lifetime of components',
    author='PGarn',
    author_email='paul.garnier@ens-rennes.fr',
    url='https://github.com/PGarn/LifeTime',
    packages=find_packages(),
    package_data={
        'PowDeRUL': ['function/*','example/*'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'numpy>=1.19.2',
        'pandas>=1.1.3',
        'scipy>=1.10.1',
        'pandas>=2.0.1',
        'matplotlib>=3.7.1',
        'numpy>=1.24.1',
        'rainflow>=3.2.0',
        'openpyxl>=3.1.2',
    ],
)
