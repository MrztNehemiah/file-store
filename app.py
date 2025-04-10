import os
import boto3
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

# AWS setup
S3_BUCKET = "nehesbucket"
s3 = boto3.client('s3')

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    
    s3.upload_fileobj(
        file,
        S3_BUCKET,
        file.filename,
        ExtraArgs={'ACL': 'public-read'}  # Optional: makes file public
    )
    
    return f'File uploaded to S3: https://{S3_BUCKET}.s3.amazonaws.com/{file.filename}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

