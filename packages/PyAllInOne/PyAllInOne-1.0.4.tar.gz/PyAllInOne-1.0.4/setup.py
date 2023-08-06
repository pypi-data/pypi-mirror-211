# PyAllInOne - Setup.py

''' This is the 'setup.py' file. '''

# Imports
from setuptools import setup, find_packages

# README.md
with open("README.md") as readme_file:
    README = readme_file.read()

# Setup Arguments
setup_args = dict (
    name = "PyAllInOne",
    version = "1.0.4",
    description = "PyAllInOne is an advanced multi-purpose Python package.",
    long_description = README,
    long_description_content_type = "text/markdown",
    license = "MIT",
    packages = find_packages(),
    include_package_data = True,
    author = "Aniketh Chavare",
    author_email = "anikethchavare@outlook.com",
    url = "https://github.com/Anikethc/PyAllInOne",
    download_url = "https://pypi.org/project/PyAllInOne",
    install_requires = [
        "screen-brightness-control",
        "opencv-python",
        "imutils",
        "numpy",
        "pytesseract",
        "pillow",
        "matplotlib"
    ],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development"
    ]
)

# Run the Setup File
if __name__ == "__main__":
    setup(**setup_args)