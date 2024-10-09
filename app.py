from flask import Flask, render_template, request, redirect, url_for
import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv() 
app = Flask(__name__)

# AWS S3 Configuration
Region = os.getenv('Region')
BucketName = os.getenv('BucketName')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
s3 = boto3.client(
   "s3",
   aws_access_key_id=AWS_ACCESS_KEY_ID,
   aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
   region_name=Region
)

# Home page for uploading images
@app.route('/')
def home():
    return render_template('upload.html')

# Upload Image Route
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    
    if file:
        s3.upload_fileobj(file, BucketName, file.filename)
        return 'Image uploaded successfully!'

# List Images Route
@app.route('/images')
def list_images():
    # List objects in the bucket
    images = s3.list_objects_v2(Bucket=BucketName).get('Contents', [])
    return render_template('list_images.html', images=images)

# Download Image Route
@app.route('/download/<filename>')
def download_image(filename):
    # Generate a download link for the image
    file_url = s3.generate_presigned_url('get_object', Params={'Bucket': BucketName, 'Key': filename}, ExpiresIn=100)
    return redirect(file_url)

if __name__ == '__main__':
    app.run(debug=True)
