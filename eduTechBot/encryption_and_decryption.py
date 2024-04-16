import csv
def encrypt_data(data):
        # Simple encryption using a substitution cipher
        encrypted_data = ''.join(chr(ord(char) + 1) for char in data)
        return encrypted_data

def decrypt_data(encrypted_data):
    # Simple decryption for the substitution cipher
    decrypted_data = ''.join(chr(ord(char) - 1) for char in encrypted_data)
    return decrypted_data

def read_encrypted_csv(file_path):
    data = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            decrypted_row = [decrypt_data(item) for item in row]
            data.append(decrypted_row)
    return data

file_path = "shubh_chat_history.csv"
print(read_encrypted_csv(file_path=file_path))