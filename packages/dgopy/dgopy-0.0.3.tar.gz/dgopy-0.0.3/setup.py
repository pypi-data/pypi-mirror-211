from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'DGo Python'
LONG_DESCRIPTION = 'DGo pilot framework data input'

setup(
    name="dgopy",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Dinh Van Luan",
    author_email="dluanvn@gmail.com",
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    keywords='dgo',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)
