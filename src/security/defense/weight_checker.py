import hashlib
import os
import datetime


def calculate_file_hash(file_path):
    if not os.path.exists(file_path):
        return None
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def generate_trusted_hash(model_path, hash_save_path="models/trusted_hash.txt"):
    # Generate and save the trusted hash for the original model
    if not os.path.exists(model_path):
        print(f"❌ Model file not found: {model_path}")
        return None

    trusted_hash = calculate_file_hash(model_path)

    with open(hash_save_path, 'w') as f:
        f.write(trusted_hash)

    print(f"✅ Trusted Hash saved at: {hash_save_path}")
    print(f"📄 Hash: {trusted_hash}")
    return trusted_hash


def verify_model(model_path, hash_ref_path="models/trusted_hash.txt"):
    # Load trusted hash from file
    if not os.path.exists(hash_ref_path):
        print("❌ Trusted hash file not found!")
        return False

    with open(hash_ref_path, 'r') as f:
        trusted_hash = f.read().strip()

    print("🛡️ Starting Integrity Verification...")

    current_hash = calculate_file_hash(model_path)

    if current_hash is None:
        print("🚨 ALERT: Model file is MISSING!")
        return False

    if current_hash == trusted_hash:
        print("✅ [STATUS: SECURE]: Model Verified. No Tampering Detected.")
        return True
    else:
        print("🚨 [CRITICAL ALERT]: WEIGHTS TAMPERING DETECTED!")
        print(f"❌ Expected Hash: {trusted_hash[:15]}...")
        print(f"❌ Current Hash:  {current_hash[:15]}...")
        print("🚫 Execution Blocked - Integrity Violation!")
        save_security_log(
            status="CRITICAL: WEIGHTS TAMPERING",
            original_hash=trusted_hash,
            current_hash=current_hash,
            model_name=os.path.basename(model_path)
        )
        return False


def save_security_log(status, original_hash, current_hash, model_name):
    log_path = "logs/security_log.txt"
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_content = f"""
{"="*50}
[SECURITY ALERT REPORT]
Timestamp: {timestamp}
Model Checked: {model_name}
Status: {status}
--------------------------------------------------
Expected Hash: {original_hash}
Current Hash:  {current_hash}
Action Taken: EXECUTION BLOCKED - Integrity Violation
{"="*50}
\n"""

    with open(log_path, "a") as f:
        f.write(log_content)

    print(f"✅ Security log saved at: {log_path}")