from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A package to Export google map data'
LONG_DESCRIPTION = '''from Gmap_data import Google_map
Google_url = "https://www.google.com/maps/search/dentist+new+york/@40.7403671,-74.0224996,13z/data=!3m1!4b1?entry=ttu"
Data_csv = "C://Users//EDITOR//Desktop//Infinity datasoft/data"
Crome_driver = "c://chromedriver.exe"
Google_map.scrap_map(Google_url,Data_csv,Crome_driver)'''

# Setting up
setup(
    name="Gmap_export",
    version=VERSION,
    author="Developer Ashok puri And Pawan yadav",
    author_email="developer1.infinity@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'tutorial', 'Google map',  'developerpawan'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
