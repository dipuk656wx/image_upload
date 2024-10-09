from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import boto3
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet, InvalidToken
import io

# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

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

# Load encryption key
encryption_key = os.getenv('ENCRYPTION_KEY').encode()
cipher = Fernet(encryption_key)

# Home page for uploading images
@app.route('/')
def home():
    return render_template('upload.html')

# Upload Image Route
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('home'))
    
    file = request.files['file']
    encrypt = request.form.get('encrypt')  # Check if the user selected encryption

    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('home'))

    if file:
        file_key = file.filename
        
        # If encryption is checked
        if encrypt == 'on':
            # Encrypt the file contents
            file_data = file.read()
            encrypted_data = cipher.encrypt(file_data)
            
            # Upload encrypted file to S3
            s3.upload_fileobj(io.BytesIO(encrypted_data), BucketName, f"encrypted/{file_key}")
            
            # Tag the file as encrypted
            s3.put_object_tagging(
                Bucket=BucketName,
                Key=f"encrypted/{file_key}",
                Tagging={'TagSet': [{'Key': 'Encrypted', 'Value': 'True'}]}
            )
        else:
            # Upload the file without encryption
            s3.upload_fileobj(file, BucketName, f"unencrypted/{file_key}")
            
            # Tag the file as unencrypted
            s3.put_object_tagging(
                Bucket=BucketName,
                Key=f"unencrypted/{file_key}",
                Tagging={'TagSet': [{'Key': 'Encrypted', 'Value': 'False'}]}
            )
        
        flash('Image uploaded successfully!', 'success')
        return redirect(url_for('list_images'))

# List Images Route (User-Specific)
@app.route('/images', methods=['GET', 'POST'])
def list_images():
    show_encrypted = request.args.get('encrypted') == 'on'  # Check if the user wants only encrypted images
    prefix = "encrypted/" if show_encrypted else ""

    # List objects in the bucket
    response = s3.list_objects_v2(Bucket=BucketName, Prefix=prefix)
    images = response.get('Contents', [])
    return render_template('list_images.html', images=images, show_encrypted=show_encrypted)

@app.route('/download/<filename>', methods=['POST'])
def download_image(filename):
    download_type = request.form['download_type']  # Get download type from form
    file_key = filename  # The key in S3

    # Get the file from S3
    try:
        response = s3.get_object(Bucket=BucketName, Key=file_key)
        file_data = response['Body'].read()

        if download_type == 'encrypted':
            # Return the encrypted file as is
            print("adfsdf")
            return send_file(
                io.BytesIO(file_data),
                attachment_filename=filename.split('/')[-1],
                as_attachment=True
            )
        elif download_type == 'decrypted':
            decryption_key = request.form.get('decryption_key')  # Get decryption key from the user
            try:
                cipher = Fernet(decryption_key.encode())  # Create a new cipher object with the provided key
                decrypted_data = cipher.decrypt(file_data)
                print(decrypted_data)
                # Return the decrypted file
                return send_file(
                    io.BytesIO(decrypted_data),
                    attachment_filename=filename.split('/')[-1],
                    as_attachment=True
                )
            except InvalidToken:
                flash('Invalid decryption key', 'danger')
                return redirect(url_for('list_images'))
        else:
            flash('Invalid download option selected', 'danger')
            return redirect(url_for('list_images'))
    except Exception as e:
        flash(f'Error retrieving file: {str(e)}', 'danger')
        return redirect(url_for('list_images'))


if __name__ == '__main__':
    app.run(debug=True)
