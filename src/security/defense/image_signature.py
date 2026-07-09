import os
import hashlib
import datetime
# pyrefly: ignore [missing-import]
from cryptography.hazmat.primitives import hashes
# pyrefly: ignore [missing-import]
from cryptography.hazmat.primitives.asymmetric import rsa, padding


# Generate RSA key pair once at startup
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()


def sign_image(image_data):
    # Sign an image with the private key
    img_hash = hashlib.sha256(image_data).digest()
    signature = private_key.sign(
        img_hash,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    return signature


def verify_image_signature(image_data, signature):
    # Verify image signature to detect tampering
    img_hash = hashlib.sha256(image_data).digest()
    try:
        public_key.verify(
            signature,
            img_hash,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return True
    except:
        return False


def scan_image(image_path, original_signature):
    # Scan a single image and verify its signature
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return False

    with open(image_path, "rb") as f:
        image_data = f.read()

    is_safe = verify_image_signature(image_data, original_signature)

    if is_safe:
        print("✅ Image is CLEAN - No tampering detected.")
    else:
        print("🚨 ALERT: Image has been TAMPERED!")
        save_security_log(image_path)

    return is_safe


def save_security_log(image_path):
    log_path = "logs/backdoor_log.txt"
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_content = f"""
{"="*50}
[BACKDOOR DEFENSE REPORT]
Timestamp: {timestamp}
Image Checked: {os.path.basename(image_path)}
Status: CRITICAL - TRIGGER DETECTED
Action Taken: IMAGE BLOCKED
{"="*50}
\n"""

    with open(log_path, "a") as f:
        f.write(log_content)

    print(f"✅ Security log saved at: {log_path}")