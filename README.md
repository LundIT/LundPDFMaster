# Lund PDF Master

A Python library for converting office files to PDF using the iLovePDF API.

## Install the package

```python
pip install LundPDFMaster
```

## Usage

Here's a basic example of how to use the library for a single file:

```python
from lund_pdf_master.OfficeToPDFConverter import OfficeToPDFConverter

converter = OfficeToPDFConverter('your_public_key', 'your_secret_key')
converter.convert_to_pdf('path_to_your_file.docx', 'output_path.pdf')
```

Here's a basic example of how to use the library for multiple files:

```python
from lund_pdf_master.OfficeToPDFConverter import OfficeToPDFConverter

converter = OfficeToPDFConverter('your_public_key', 'your_secret_key')
file_paths = ['file1.docx', 'file2.docx', 'file3.docx']
converter.convert_multiple_to_pdf(file_paths, 'output_directory')
```

This project is licensed under the terms of the MIT license
