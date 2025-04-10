import boto3
from flask import Flask, request, render_template

app = Flask(__name__)

S3_BUCKET = "nehesbucket"
REGION = "us-east-1"

s3 = boto3.client("s3")

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "❌ No file part in the request", 400

    file = request.files['file']
    if file.filename == '':
        return "❌ No file selected", 400

    try:
        s3.upload_fileobj(
            file,
            S3_BUCKET,
            file.filename,
        )

        file_url = f"https://{S3_BUCKET}.s3.{REGION}.amazonaws.com/{file.filename}"
        return f"✅ Uploaded successfully: <a href='{file_url}'>{file.filename}</a>"

    except Exception as e:
        print(f"Upload error: {e}")
        return f"❌ Upload failed: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

