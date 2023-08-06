from setuptools import setup, find_packages

VERSION = '0.0.99.3' 
DESCRIPTION = 'IC50 prediction'
LONG_DESCRIPTION = 'Calculate IC50/pIC50 values using a variety of methods.'

setup(
        name="ic50", 
        version=VERSION,
        author="Steve Niu",
        author_email="<niuacademics@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['numpy','scipy','matplotlib',''],
        keywords=['python', 'IC50'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)