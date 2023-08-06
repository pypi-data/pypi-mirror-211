from setuptools import setup, find_packages


setup(
    name='PowDeRUL',
    version='1.0.16',
    license='MIT',
    author='PGarn',
    author_email='paul.garnier@ens-rennes.fr',
    url='https://github.com/PGarn/LifeTime',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'numpy>=1.19.2,<1.24.0',
        'pandas>=1.1.3,<2.0.0',
        'scipy>=1.10.1,<2.0.0',
        'matplotlib>=3.7.1,<4.0.0',
        'rainflow==3.2.0',
        'openpyxl==3.1.2',
    ],
)
