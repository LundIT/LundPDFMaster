from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="LundPDFMaster",
    version="1.2.0",
    author="Ensar Kaya",
    author_email="e.kaya@lund-it.com",
    description="A Python library for converting office files to PDF using the iLovePDF API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LundIT/LundPDFMaster",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
    ],
    python_requires='>=3.6',
)
