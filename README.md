# ilovepdf_python

A Python library for converting office files to PDF using the iLovePDF API.

## Usage

Here's a basic example of how to use the library for a single file:

```python
from lund_pdf_master import OfficeToPDFConverter

converter = OfficeToPdfConverter('your_public_key', 'your_secret_key')
converter.convert_to_pdf('path_to_your_office_file', 'path_to_output_pdf')
```

Here's a basic example of how to use the library for multiple files:

```python
converter = OfficeToPdfConverter('your_public_key', 'your_secret_key')
# List of file paths to convert
file_paths = [
    'file1.docx',
    'file2.pptx',
    'file3.xlsx'
]

output_path = 'output.zip'
converter.convert_bulk_to_pdf(file_paths, output_path)
```
