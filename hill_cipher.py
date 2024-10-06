import numpy as np

def create_key_matrix(key):
    key = key.upper().replace(' ', '')
    key_matrix = np.array([ord(c) - 65 for c in key]).reshape(2, 2)
    return key_matrix

def hill_encrypt(message, key_matrix):
    message = message.upper().replace(' ', '')  # Convert message to uppercase
    message_vector = [ord(c) - 65 for c in message]
    
    # Ensure the message length is a multiple of the key matrix dimension
    n = key_matrix.shape[0]
    padding_length = (n - (len(message_vector) % n)) % n
    message_vector.extend([0] * padding_length)  # Pad with zeros

    encrypted_message = ""
    for i in range(0, len(message_vector), n):
        block = np.array(message_vector[i:i + n])
        block = block.reshape(n, 1)  # Ensure block is a column vector
        encrypted_block = np.dot(key_matrix, block) % 26
        encrypted_message += ''.join(chr(num[0] + 65) for num in encrypted_block)
    
    return encrypted_message

def hill_decrypt(encrypted_message, key_matrix):
    key_matrix = np.array(key_matrix)
    
    # Compute modular inverse of the key matrix
    def mod_inv(matrix, mod):
        det = int(np.round(np.linalg.det(matrix)))
        det_inv = pow(det, -1, mod)
        matrix_inv = np.round(np.linalg.inv(matrix) * det).astype(int) % mod
        return (matrix_inv * det_inv) % mod

    key_matrix_inv = mod_inv(key_matrix, 26)
    
    encrypted_vector = [ord(c) - 65 for c in encrypted_message]
    
    # Ensure the encrypted message length is a multiple of the key matrix dimension
    n = key_matrix.shape[0]
    padding_length = (n - (len(encrypted_vector) % n)) % n
    encrypted_vector.extend([0] * padding_length)  # Pad with zeros
    
    decrypted_message = ""
    for i in range(0, len(encrypted_vector), n):
        block = np.array(encrypted_vector[i:i + n])
        block = block.reshape(n, 1)  # Ensure block is a column vector
        decrypted_block = np.dot(key_matrix_inv, block) % 26
        decrypted_message += ''.join(chr(num[0] + 65) for num in decrypted_block)
    
    # Convert back to lowercase and return
    return decrypted_message.lower()
