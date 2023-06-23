import os
import unittest
from lund_pdf_master.OfficeToPDFConverter import OfficeToPdfConverter


class TestPdfConverter(unittest.TestCase):
    def setUp(self):
        self.converter = OfficeToPdfConverter(
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
        server_filename = self.converter.upload_file(server, task, "tests/test.docx")
        self.assertIsInstance(server_filename, str)

    def test_full_usage(self):
        # Assuming you have a test file at 'tests/test.docx'
        self.converter.convert_to_pdf("tests/test.docx", "output.pdf")
        # Check that the output file exists
        self.assertTrue(os.path.exists("output.pdf"))


if __name__ == "__main__":
    unittest.main()
