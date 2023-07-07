import os
import unittest
from lund_pdf_master.OfficeToPDFConverter import OfficeToPDFConverter


class TestPdfConverter(unittest.TestCase):
    def setUp(self):
        self.converter = OfficeToPDFConverter(
            "public_key",
            "secret_key",
        )

    def test_get_auth_token(self):
        token = self.converter.get_auth_token()
        self.assertIsInstance(token, str)

    def test_start_task(self):
        server, task = self.converter.start_task("officepdf")
        self.assertIsInstance(server, str)
        self.assertIsInstance(task, str)

    def test_upload_file(self):
        # Assuming you have a test file at 'test.docx'
        server, task = self.converter.start_task("officepdf")
        server_filename = self.converter.upload_file(server, task, "tests/file1.docx")
        self.assertIsInstance(server_filename, str)

    def test_full_usage(self):
        # Assuming you have a test file at 'tests/test.docx'
        self.converter.convert_to_pdf("tests/file1.docx", "output.pdf")
        # Check that the output file exists
        self.assertTrue(os.path.exists("output.pdf"))


    def test_convert_multiple_to_pdf(self):
        # List of file paths to convert
        file_paths = [
            'tests/input/file1.docx',
            'tests/input/file2.docx',
            'tests/input/file3.docx'
        ]

        # Output directory for the resulting PDF files
        output_dir = 'tests/output'

        # Perform multiple conversions
        self.converter.convert_multiple_to_pdf(file_paths, output_dir)

        # Assert that the output PDF files exist
        for file_path in file_paths:
            filename = os.path.splitext(os.path.basename(file_path))[0] + '.pdf'
            output_path = os.path.join(output_dir, filename)
            self.assertTrue(os.path.exists(output_path))

        # Clean up: delete the output PDF files
        for file_path in file_paths:
            filename = os.path.splitext(os.path.basename(file_path))[0] + '.pdf'
            output_path = os.path.join(output_dir, filename)
            os.remove(output_path)

if __name__ == "__main__":
    unittest.main()
