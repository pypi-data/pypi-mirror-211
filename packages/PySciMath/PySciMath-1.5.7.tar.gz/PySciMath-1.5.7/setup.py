# PySciMath - Setup.py

''' This is the 'setup.py' file. '''

# Imports
from setuptools import setup, find_packages

# README.md
with open("README.md") as readme_file:
    README = readme_file.read()

# Setup Arguements
setup_args = dict (
    name="PySciMath",
    version="1.5.7",
    description="PySciMath is a general-purpose Python package to work on calculations and solve mathmematical and scientific problems.",
    long_description_content_type="text/markdown",
    long_description=README,
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    author="Aniketh Chavare",
    author_email="anikethchavare@outlook.com",
    keywords=["Math", "Mathematics", "Science", "Calculations"],
    url="https://github.com/Anikethc/PySciMath",
    download_url="https://pypi.org/project/PySciMath"
)

# Install Requires
install_requires = ["matplotlib", "numpy"]

# Run the Setup File
if __name__ == "__main__":
    setup(**setup_args, install_requires=install_requires)