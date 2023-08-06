from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'General framework for estimating waste quantities in time.'
LONG_DESCRIPTION = 'Package that offers a general framework for estimating radioactive waste quantities in time and enables the modeling of various waste management strategies.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="wastimate", 
        version=VERSION,
        author="Hando Tohver",
        author_email="<handotohver@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['numpy', 'scipy'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'radioactive waste', 'Modeling'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
            "License :: OSI Approved :: MIT License"
        ]
)