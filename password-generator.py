import random
import string

def generate_password(length=8):
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation

    # Combine all character sets
    all_chars = lowercase + uppercase + digits + symbols

    # Generate password
    password = ''.join(random.choice(all_chars) for _ in range(length))

    return password

# Example usage:
print(generate_password(15))