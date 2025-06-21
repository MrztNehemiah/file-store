import os
import boto3
from flask import Flask, request, render_template

app = Flask(__name__)

# AWS setup
S3_BUCKET = "nehesbucket"
REGION = "us-east-1"
s3 = boto3.client('s3')


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part in the request.'

    file = request.files['file']

    if file.filename == '':
        return 'No file selected.'

    # Upload to S3
    s3.upload_fileobj(
        file,
        S3_BUCKET,
        file.filename
    )

    file_url = f"https://{S3_BUCKET}.s3.{REGION}.amazonaws.com/{file.filename}"
    return f'✅ File uploaded to S3: <a href="{file_url}">{file.filename}</a>'


@app.route('/files')
def list_files():
    try:
        files = s3.list_objects_v2(Bucket=S3_BUCKET)

        file_urls = []
        for obj in files.get('Contents', []):
            key = obj['Key']
            file_url = f"https://{S3_BUCKET}.s3.{REGION}.amazonaws.com/{key}"
            file_urls.append(file_url)

        return render_template('files.html', files=file_urls)

    except Exception as e:
        print(f"List error: {e}")
        return f"❌ Could not list files: {str(e)}", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

