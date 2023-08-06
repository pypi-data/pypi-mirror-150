from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = "Brian's first Python package"
LONG_DESCRIPTION = "Brian's first Python package with a slightly longer description"

# Setting up
setup(
       # the name must match the folder name 'briansfirstpackage'
        name="briansfirstpackage02", 
        version=VERSION,
        author="Brian Hassard",
        author_email="<iamthebriguy@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)