from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A package that provides functions to retrieve IP geolocation information.'

# Setting up
setup(
    name="ippython",
    version=VERSION,
    author="Aneko",
    author_email="anekobtww@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'bs4'],
    keywords=['python', 'ip', 'geography', 'city', 'country'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)