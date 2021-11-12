from flask import Flask

app = Flask(__name__)


from flask import request
from werkzeug.utils import secure_filename

from google.cloud import storage
from google.auth.credentials import AnonymousCredentials
from gcp_storage_emulator.server import create_server
from flask import jsonify, make_response
from datetime import datetime, timezone
import json
import os





HOST = "localhost"
PORT = 9023
BUCKET = "xpl_emp_api"
FILESIZE = 10000000 # 10 MB (minimum)
FORMATS = {'doc', 'docx', 'pdf'}
GCP_CREDENTIALS_PATH = 'C:/hjsoftware/test workflow/xplur-employment-api/xplur-employment-api-fc86a98d253f.json'



@app.route('/upload', methods=['POST'])
def upload_resume():
    ''' Uploading File in GCP Stroage'''
    try:
        datetimestamp = datetime.now(timezone.utc).astimezone().isoformat()
        if request.method == 'POST':
            file = request.files['file']
            ########  file format checking ###########
            file_extension = file.filename.split(".")[1]    
            if file_extension.lower() in FORMATS:
                blob = request.files['file'].read()
                file_size = len(blob)
                if file_size <= FILESIZE:  
                    extension = secure_filename(file.filename).rsplit('.', 1)[1]
                    gcs = storage.Client.from_service_account_json(GCP_CREDENTIALS_PATH)
                    bucket = gcs.get_bucket(BUCKET)
                    blob = bucket.blob(file.filename)
                    blob.upload_from_file(file) # GCP Stroage accept upto 5 TiB
                    path = '/' + BUCKET + '/' + str(secure_filename(file.filename))
                    if file and allowed_file(file.filename):
                       
                        with gcs.open(path, 'w') as f:
                            f.write(file.stream.read())# instead of f.write(str(file))
                            data = {'timestamp': datetimestamp,'status': 201,"success":True,"message": "File uploading Successfully"}
                            return make_response(jsonify(data))
                        
                else:
                    data = {'timestamp': datetimestamp,'status': 400 ,"error": "Bad Request","message": "file size more then 10 MB"}
                    return make_response(jsonify(data))
                        
            else:
                data = {'timestamp': datetimestamp,'status': 404,"error": "the requested resource does not exist","message": "you can upload file invalid format"}
                return make_response(jsonify(data))
    except Exception as e:
        data = {'timestamp': datetimestamp,'status': e.code.value,"error":e.errors,"message": e.message}
        return make_response(jsonify(data))

        ###############


if __name__ == "__main__":
	app.run(host='127.0.0.1', port=5000)







#  