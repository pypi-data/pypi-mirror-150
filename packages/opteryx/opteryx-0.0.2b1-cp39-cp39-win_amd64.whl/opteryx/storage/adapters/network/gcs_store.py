import os

from typing import Optional

from opteryx.exceptions import MissingDependencyError
from opteryx.storage import BaseStorageAdapter
from opteryx.utils import paths

try:
    from google.auth.credentials import AnonymousCredentials
    from google.cloud import storage

    GOOGLE_CLOUD_STORAGE_INSTALLED = True
except ImportError:  # pragma: no cover
    GOOGLE_CLOUD_STORAGE_INSTALLED = False


class GcsStorage(BaseStorageAdapter):
    def __init__(self, project: Optional[str] = None, credentials=None, **kwargs):
        if not GOOGLE_CLOUD_STORAGE_INSTALLED:  # pragma: no cover
            raise MissingDependencyError(
                "`google-cloud-storage` is missing, please install or include in requirements.txt"
            )

        #        super().__init__(**kwargs)
        self.project = project
        self.credentials = credentials

    def read_blob(self, blob_name):
        import io

        bucket, object_path, name, extension = paths.get_parts(blob_name)
        bucket = bucket.replace("_data", "-data")

        blob = get_blob(
            project=self.project,
            bucket=bucket,
            blob_name=object_path + name + extension,
        )
        stream = blob.download_as_bytes()
        return io.BytesIO(stream)

    def get_blob_list(self, partition):
        bucket, object_path, name, extension = paths.get_parts(partition)
        bucket = bucket.replace("_data", "-data")

        # print(bucket, object_path, name, extension)

        # this means we're not actually going to GCP
        if os.environ.get("STORAGE_EMULATOR_HOST") is not None:
            client = storage.Client(
                credentials=AnonymousCredentials(),
                project=self.project,
            )
        else:  # pragma: no cover
            client = storage.Client(project=self.project)

        gcs_bucket = client.get_bucket(bucket)
        blobs = list(client.list_blobs(bucket_or_name=gcs_bucket, prefix=object_path))

        yield from [
            bucket + "/" + blob.name for blob in blobs if not blob.name.endswith("/")
        ]


def get_blob(project: str, bucket: str, blob_name: str):

    # this means we're not actually going to GCP
    if os.environ.get("STORAGE_EMULATOR_HOST") is not None:
        client = storage.Client(
            credentials=AnonymousCredentials(),
            project=project,
        )
    else:  # pragma: no cover
        client = storage.Client(project=project)

    gcs_bucket = client.get_bucket(bucket)
    blob = gcs_bucket.get_blob(blob_name)
    return blob
