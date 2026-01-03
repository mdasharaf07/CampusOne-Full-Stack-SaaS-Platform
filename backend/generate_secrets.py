import secrets
import os
import sys
import shutil
from datetime import datetime

def check_dependencies():
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.fernet import Fernet
        return True
    except ImportError:
        print("\033[91m❌ Error: 'cryptography' library not found.\033[0m")
        print("Please install it using: \033[96mpip install cryptography python-dotenv\033[0m")
        return False

def generate_secrets():
    if not check_dependencies():
        return

    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.fernet import Fernet

    # Professional ASCII Header
    print("\033[95m")
    print("  🔒 SECURE KEY GENERATOR 🔒")
    print("  ==========================")
    print("\033[0m")

    # 1. Generate JWT Secret (64 bytes -> 128 hex chars)
    jwt_secret = secrets.token_hex(64)
    print("✅ JWT Secret Generated")

    # 2. Generate Symmetric Encryption Key (Fernet/AES)
    encryption_key = Fernet.generate_key().decode('utf-8')
    print("✅ Symmetric Encryption Key Generated")

    # 3. Generate RSA Key Pair (Asymmetric)
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    
    # Export Private Key to PEM
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

    # Export Public Key to PEM
    pem_public = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    print("✅ RSA 2048-bit Key Pair Generated")

    # Path to .env file
    env_path = '.env'

    # 4. Backup existing .env
    if os.path.exists(env_path):
        backup_path = f".env.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy(env_path, backup_path)
        print(f"📦 Created backup of existing .env: \033[90m{backup_path}\033[0m")

    # Prepare the data
    secrets_dict = {
        "JWT_SECRET": jwt_secret,
        "CRYPTO_KEY": encryption_key,
        "RSA_PRIVATE_KEY": pem_private.replace('\n', '\\n'),
        "RSA_PUBLIC_KEY": pem_public.replace('\n', '\\n')
    }

    # Update or create .env file
    try:
        from dotenv import set_key, load_dotenv
        
        # Ensure file exists
        if not os.path.exists(env_path):
            with open(env_path, 'w') as f:
                pass
        
        for key, value in secrets_dict.items():
            set_key(env_path, key, value)
            
        print("\033[92m\n✨ SUCCESS: Keys automatically stored in .env\033[0m")
        
    except ImportError:
        # Fallback if python-dotenv is not installed (though it should be)
        print("\033[93m\n⚠️ python-dotenv not found. Writing to .env manually...\033[0m")
        
        existing_lines = []
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                existing_lines = f.readlines()

        # Simple update logic
        new_lines = []
        keys_handled = set()
        
        for line in existing_lines:
            handled = False
            for key in secrets_dict:
                if line.startswith(f"{key}="):
                    new_lines.append(f"{key}=\"{secrets_dict[key]}\"\n")
                    keys_handled.add(key)
                    handled = True
                    break
            if not handled:
                new_lines.append(line)
        
        for key, value in secrets_dict.items():
            if key not in keys_handled:
                new_lines.append(f"{key}=\"{value}\"\n")

        with open(env_path, 'w') as f:
            f.writelines(new_lines)
            
        print("\033[92m\n✨ SUCCESS: Keys manually written to .env\033[0m")

    print("\033[94m" + "="*50 + "\033[0m")
    print("\033[91m⚠️  WARNING: Never commit your .env file to Git!\033[0m")
    print("\033[94m" + "="*50 + "\033[0m")

if __name__ == "__main__":
    generate_secrets()
