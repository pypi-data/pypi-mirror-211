from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'A package to convert pdf .mhtml,mhtm,xml,igs,htm,pdf,csv,xlsb,xls,xlsx,doc,docx,dotx,rtf,txt,plist,png,jpg,tif,gif,pptx,ppt support extension'
LONG_DESCRIPTION = '''from pdfgen import Topdftool 
input_folder_path = 'C://Users/EDITOR/Desktop/input29'
output_folder_path = 'C://Users/EDITOR/Desktop/output29'
Topdftool.scrape_files(input_folder_path, output_folder_path)'''

# Setting up
setup(
    name="Topdfgen",
    version=VERSION,
    author="Developer Ashok puri And Pawan yadav",
    author_email="developer1.infinity@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'tutorial', 'convert to pdf',  'developerpawan'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
