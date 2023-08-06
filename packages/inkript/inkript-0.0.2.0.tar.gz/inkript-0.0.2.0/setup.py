from setuptools import setup, find_packages
import codecs
import os

version = "0.0.2.0"

description = "to create keys to encrypt and decrypt files"

with open( "README.md", "r" ) as f:
    long_description = f.read( )

# setting up
setup(
     name = "inkript"
    , version = version
    , author = "mose_tucker_0159"
    , author_email = "mose.tucker.0159@gmail.com"
    , description = description
    , long_description = long_description
    , long_description_content_type = "text/markdown"
    , packages = find_packages( )
    , install_requires = [
         "cryptography"
      ]
    , keywords = [ "python" ]
    , classifiers = [
         "Development Status :: 1 - Planning"
        , "Intended Audience :: End Users/Desktop"
        , "Programming Language :: Python :: 3"
        , "Operating System :: Microsoft :: Windows"
        , "Operating System :: MacOS"
      ]
)
