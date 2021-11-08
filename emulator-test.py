from google.auth.credentials import AnonymousCredentials
from google.cloud import storage
from gcp_storage_emulator.server import create_server

HOST = "localhost"
PORT = 9023
BUCKET = "test-bucket"

# default_bucket parameter creates the bucket automatically
server = create_server(HOST, PORT, in_memory=True, default_bucket=BUCKET)
server.start()

client = storage.Client(
    credentials=AnonymousCredentials(),
    project="test",
)
bucket = client.bucket(BUCKET)
import ipdb; ipdb.set_trace()
blob = bucket.blob("blob1")
blob.upload_from_string("test1")
blob = bucket.blob("blob2")
blob.upload_from_string("test2")
for blob in bucket.list_blobs():
    content = blob.download_as_bytes()
    print("Blob [{}]: {}".format(blob.name, content))

server.stop()