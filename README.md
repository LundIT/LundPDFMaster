# ilovepdf_python

A Python library for converting office files to PDF using the iLovePDF API.

## Usage

Here's a basic example of how to use the library:

```python
from pdfmaster import OfficeToPdfConverter

converter = OfficeToPdfConverter('your_public_key', 'your_secret_key')
converter.convert_to_pdf('path_to_your_office_file', 'path_to_output_pdf')
```
