from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def helloIndex():
    return 'Hello World from Python Flask!'




from flask import request
from werkzeug.utils import secure_filename

from google.cloud import storage

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
    	import ipdb; ipdb.set_trace()
    	#storage_client = storage.Client.from_service_account_json('C:/hjsoftware/test workflow/xplur-employment-api/sharp-haven-330914-5b83655e530a.json')
    	# buckets = list(storage_client.list_buckets())
    	# print(buckets)
    	# C:\hjsoftware\test workflow\xplur-employment-api
    	# try:
    	# 	bucket_name = storage_client.get_bucket("xlpuremployent-bucket")
    	# except:
    	# 	bucket_name =storage_client.create_bucket("xlpuremployent-bucket") 
    	file = request.files['file']
    	extension = secure_filename(file.filename).rsplit('.', 1)[1]
    	options = {}
    	gcs = storage.Client.from_service_account_json('C:/hjsoftware/test workflow/xplur-employment-api/sharp-haven-330914-5b83655e530a.json')
    	options['retry_params'] = gcs.RetryParams(backoff_factor=1.1)
    	options['content_type'] = 'image/' + extension
    	bucket_name = "gcs-tester-app"
    	path = '/' + bucket_name + '/' + str(secure_filename(file.filename))
    	if file and allowed_file(file.filename):
            try:
                with gcs.open(path, 'w', **options) as f:
                    f.write(file.stream.read())# instead of f.write(str(file))
                    print(jsonify({"success": True}))
                return jsonify({"success": True})
            except Exception as e:
                logging.exception(e)
                return jsonify({"success": False})

if __name__ == "__main__":
	app.run(host='127.0.0.1', port=5000)
