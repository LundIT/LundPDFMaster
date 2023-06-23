from setuptools import setup, find_packages

setup(
    name="LundPDFMaster",
    version="0.1",
    packages=["lund_pdf_master"],
    url="https://github.com/LundIT/LundPDFMaster",
    license="MIT",
    author="Ensar Kaya",
    author_email="ensarben@gmail.com",
    description="A Python library for converting office files to PDF using the iLovePDF API",
    install_requires=[
        "requests",
    ],
)
