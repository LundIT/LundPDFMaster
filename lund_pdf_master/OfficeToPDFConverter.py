import os
import traceback
import requests
import logging
import concurrent.futures
from rest_framework.exceptions import APIException
import io


class OfficeToPDFConverter:
    def __init__(self, public_key, secret_key):
        """
        Initialize the converter with the public and secret keys.

        Parameters:
        public_key (str): The public key for the iLovePDF API.
        secret_key (str): The secret key for the iLovePDF API.
        """
        self.public_key = public_key
        self.secret_key = secret_key
        self.base_url = "https://api.ilovepdf.com/v1/"
        logging.basicConfig(level=logging.INFO)

    def get_auth_token(self):
        """
        Get the authentication token from the iLovePDF API.

        Returns:
        str: The authentication token.
        """
        url = self.base_url + "auth"
        data = {"public_key": self.public_key}
        response = requests.post(url, data=data)
        data = response.json()
        return data["token"]

    def get_headers(self):
        """
        Get the headers for the API requests.

        Returns:
        dict: The headers for the API requests.
        """
        return {"Authorization": "Bearer " + self.get_auth_token()}

    def start_task(self, tool):
        """
        Start a new task with the specified tool.

        Parameters:
        tool (str): The name of the tool to use.

        Returns:
        tuple: The server and task ID for the new task.
        """
        url = self.base_url + "start/" + tool
        response = requests.get(url, headers=self.get_headers())
        data = response.json()
        return data["server"], data["task"]

    def upload_file(self, server, task, file_path):
        """
        Upload a file to the iLovePDF API.

        Parameters:
        server (str): The server to upload the file to.
        task (str): The task ID to associate with the file.
        file_path (str): The path of the file to upload.

        Returns:
        str: The server filename of the uploaded file.
        """
        url = f"https://{server}/v1/upload"
        data = {"task": task}
        if os.getenv("STORAGE_TYPE") == "SHAREPOINT":
            from django.core.files.storage import default_storage
            from django.core.files import File
            with default_storage.open(file_path, "rb") as f:
                files = {"file": File(io.BytesIO(f.read()), name=os.path.basename(file_path))}
                response = requests.post(
                    url, headers=self.get_headers(), files=files, data=data
                )
        else:
            with open(file_path, "rb") as f:
                files = {"file": f}
                response = requests.post(
                    url, headers=self.get_headers(), files=files, data=data
                )
        return response.json()["server_filename"]

    def process_file(self, server, task, server_filename):
        """
        Process the uploaded file with the specified tool.

        Parameters:
        server (str): The server where the file was uploaded.
        task (str): The task ID associated with the file.
        server_filename (str): The server filename of the file.

        Returns:
        dict: The response from the API.
        """
        url = f"https://{server}/v1/process"
        data = {
            "task": task,
            "tool": "officepdf",
            "files": [{"server_filename": server_filename, "filename": "output.pdf"}],
        }
        response = requests.post(url, headers=self.get_headers(), json=data)
        return response.json()

    def process_files(self, server, task, server_filenames):
        """
        Process the uploaded files with the specified tool.

        Parameters:
        server (str): The server where the files were uploaded.
        task (str): The task ID associated with the files.
        server_filenames (list[str]): The server filenames of the files.

        Returns:
        dict: The response from the API.
        """
        url = f"https://{server}/v1/process"
        files = [{"server_filename": filename, "filename": f"{filename}.pdf"} for server_filename, filename in
                 server_filenames]
        data = {
            "task": task,
            "tool": "officepdf",
            "files": files,
        }
        response = requests.post(url, headers=self.get_headers(), json=data)
        return response.json()

    def download_file(self, server, task, output_path):
        """
        Download the processed file from the iLovePDF API.

        Parameters:
        server (str): The server where the file was processed.
        task (str): The task ID associated with the file.
        output_path (str): The path where the file should be saved.
        """
        url = f"https://{server}/v1/download/{task}"
        response = requests.get(url, headers=self.get_headers())
        if os.getenv("STORAGE_TYPE") == "SHAREPOINT":
            from django.core.files.storage import default_storage
            from django.core.files import File

            default_storage.save(output_path,
                                 content=File(io.BytesIO(response.content), name=os.path.basename(output_path)))
        else:
            with open(output_path, "wb") as f:
                f.write(response.content)

    def convert_to_pdf(self, file_path: str, output_path: str) -> None:
        """
        Convert an office file to a PDF.

        This method performs the following steps:
        1. Starts a new 'officepdf' task.
        2. Uploads the office file to the iLovePDF API.
        3. Processes the uploaded file with the 'officepdf' tool.
        4. Downloads the processed file from the iLovePDF API.

        Parameters:
        file_path (str): The path of the office file to convert.
        output_path (str): The path where the PDF should be saved.

        Returns:
        None
        """
        # Create output directory if it doesn't exist
        if os.getenv("STORAGE_TYPE") == "SHAREPOINT":
            from django.core.files.storage import default_storage
            from django.core.files import File
            if not default_storage.exists(f"{os.path.dirname(output_path)}/"):
                default_storage.save(os.path.dirname(output_path) + '/dummy.txt',
                                     content=File(io.BytesIO(), name='dummy.txt'))
                default_storage.delete(os.path.dirname(output_path) + '/dummy.txt')
        else:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
        try:
            logging.info("Starting conversion task...")
            server, task = self.start_task("officepdf")
            logging.info("Task started successfully.")

            logging.info("Uploading file...")
            server_filename = self.upload_file(server, task, file_path)
            logging.info("File uploaded successfully.")

            logging.info("Processing file...")
            self.process_file(server, task, server_filename)
            logging.info("File processed successfully.")

            logging.info("Downloading file...")
            self.download_file(server, task, output_path)
            logging.info("File downloaded successfully.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise APIException({"error": f"An error occurred:", "traceback": traceback.format_exc()})

    def convert_multiple_to_pdf(self, file_paths, output_dir):
        """
        Convert multiple office files to PDF.
        """
        # Create output directory if it doesn't exist
        if os.getenv("STORAGE_TYPE") == "SHAREPOINT":
            from django.core.files.storage import default_storage
            from django.core.files import File
            if not default_storage.exists(f"{output_dir}"):
                default_storage.save(output_dir + 'dummy.txt', content=File(io.BytesIO(), name='dummy.txt'))
                default_storage.delete(output_dir + 'dummy.txt')
        else:
            os.makedirs(output_dir, exist_ok=True)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for file_path in file_paths:
                filename = os.path.splitext(os.path.basename(file_path))[
                    0]  # Get the original filename without the extension
                output_path = os.path.join(output_dir, f"{filename}.pdf")
                futures.append(executor.submit(self.convert_to_pdf, file_path, output_path))

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"An error occurred: {e}")



