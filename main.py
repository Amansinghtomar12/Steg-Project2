import numpy as np
from PIL import Image
from hill_cipher import create_key_matrix, hill_encrypt, hill_decrypt

def encode_message(image_file, message):
    # Save the uploaded image
    temp_image_path = 'static/temp_image.png'
    image_file.save(temp_image_path)
    
    # Encode message into image
    key = 'HILL'
    key_matrix = create_key_matrix(key)
    encoded_message = hill_encrypt(message, key_matrix)
    
    # Read image
    image = Image.open(temp_image_path)
    image_data = np.array(image)
    
    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in encoded_message) + '11111111'  # Adding end marker
    
    # Flatten the image array and encode the message
    flat_image_data = image_data.flatten()
    message_length = len(binary_message)
    
    for i in range(message_length):
        if binary_message[i] == '1':
            flat_image_data[i] |= 1
        else:
            flat_image_data[i] &= ~1
    
    # Reshape and save the new image
    new_image_data = flat_image_data.reshape(image_data.shape)
    new_image = Image.fromarray(new_image_data)
    encoded_image_path = 'static/encoded_image.png'
    new_image.save(encoded_image_path)
    
    return encoded_image_path

def decode_message(image_file, key_matrix):
    # Load the image and extract the data
    image = Image.open(image_file)
    image_data = np.array(image)
    flat_image_data = image_data.flatten()

    # Extract binary message from the least significant bits
    binary_message = ''
    for i in range(len(flat_image_data)):
        binary_message += str(flat_image_data[i] & 1)
    
    # Find the end marker
    end_marker = '11111111'
    end_marker_index = binary_message.find(end_marker)
    if end_marker_index == -1:
        return "End marker not found in the binary message.", None
    
    binary_message = binary_message[:end_marker_index]

    # Convert binary message to text
    try:
        # Convert binary message to bytes
        message_bytes = int(binary_message, 2)
        message_length = len(binary_message) // 8
        message_bytes = message_bytes.to_bytes(message_length, byteorder='big')
        
        # Decode the message (encrypted message)
        encrypted_message = message_bytes.decode('utf-8')
        
        # Decrypt the message using hill cipher
        decoded_message = hill_decrypt(encrypted_message, key_matrix)
    except UnicodeDecodeError:
        decoded_message = "Error decoding message. The message may be corrupted or contain invalid characters."
        encrypted_message = None
    except Exception as e:
        decoded_message = f"An error occurred: {str(e)}"
        encrypted_message = None
    
    return encrypted_message, decoded_message
