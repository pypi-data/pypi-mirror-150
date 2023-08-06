from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Lots of simple aerodynamics calculations, all in one place.'
LONG_DESCRIPTION = ''

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="aerodynamicspy", 
        version=VERSION,
        author="Mark C. Anderson",
        author_email="anderson.mark.az@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(exclude=['tests']),
        install_requires=['numpy'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'aerodynamics'],
        classifiers= [
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "License :: OSI Approved :: MIT License",
            "Topic :: Scientific/Engineering",
            "Topic :: Scientific/Engineering :: Physics"
        ]
)
