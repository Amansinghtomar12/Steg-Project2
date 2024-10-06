from flask import Flask, render_template, request, redirect, url_for
from main import encode_message, decode_message
from hill_cipher import create_key_matrix

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    image_file = request.files['image']
    message = request.form['message']
    encoded_image_path = encode_message(image_file, message)
    return redirect(url_for('home'))

@app.route('/decode', methods=['POST'])
def decode():
    image_file = request.files['image']
    key = 'HILL'  # Ensure the same key used for encoding
    key_matrix = create_key_matrix(key)
    encrypted_message, decoded_message = decode_message(image_file, key_matrix)
    return render_template('index.html', encrypted_message=encrypted_message, decoded_message=decoded_message)


if __name__ == '__main__':
    app.run(debug=True)

