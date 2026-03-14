from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import hashlib
import os


class FileChecksumOperator(BaseOperator):
    """
    Computes the checksum (MD5 or SHA256) of a file and pushes the result to XCom.

    :param file_path: The path to the file to checksum
    :param algorithm: The hashing algorithm to use (md5 or sha256)
    """

    @apply_defaults
    def __init__(self, file_path, algorithm="md5", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_path = file_path
        self.algorithm = algorithm.lower()

    def execute(self, context):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")

        hash_func = hashlib.md5() if self.algorithm == "md5" else hashlib.sha256()

        with open(self.file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)

        checksum = hash_func.hexdigest()
        self.log.info(f"Checksum ({self.algorithm}) for {self.file_path}: {checksum}")
        # Push the checksum to XCom so downstream tasks can use it
        return checksum