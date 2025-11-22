import os
import hashlib
import json
import sys
import time

# Configuration
BASELINE_FILE = "sentinel_baseline.json"

def calculate_file_hash(filepath):
    """Calculates the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Read the file in chunks to avoid using too much RAM for large files
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None

def scan_directory(directory):
    """Scans a directory and creates a dictionary of filename: hash."""
    files_state = {}
    print(f"[*] Scanning directory: {directory}...")
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            # Skip the baseline file itself if it's in the same directory
            if BASELINE_FILE in filepath:
                continue
                
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                files_state[filepath] = file_hash
                
    return files_state

def create_baseline(directory):
    """Creates the initial baseline file."""
    state = scan_directory(directory)
    with open(BASELINE_FILE, 'w') as f:
        json.dump(state, f, indent=4)
    print(f"[+] Baseline created successfully with {len(state)} files tracked.")
    print(f"[+] Saved to {BASELINE_FILE}")

def monitor_integrity(directory):
    """Compares current state against the baseline."""
    if not os.path.exists(BASELINE_FILE):
        print("[-] No baseline found. Please run 'init' first.")
        return

    print("[*] Loading baseline...")
    with open(BASELINE_FILE, 'r') as f:
        baseline_state = json.load(f)

    current_state = scan_directory(directory)
    
    print("\n--- INTEGRITY REPORT ---")
    changes_detected = False

    # Check for modified or deleted files
    for filepath, initial_hash in baseline_state.items():
        if filepath not in current_state:
            print(f"[!] DELETED: {filepath}")
            changes_detected = True
        elif current_state[filepath] != initial_hash:
            print(f"[!] MODIFIED: {filepath}")
            changes_detected = True

    # Check for new files
    for filepath in current_state:
        if filepath not in baseline_state:
            print(f"[!] NEW FILE DETECTED: {filepath}")
            changes_detected = True

    if not changes_detected:
        print("[OK] No changes detected. System is clean.")
    else:
        print("\n[WARNING] Integrity deviations detected!")

def main():
    if len(sys.argv) < 3:
        print("Usage: python sentinel.py <mode> <directory_to_watch>")
        print("Modes: \n  init    -> Create a new baseline\n  check   -> Check for changes")
        return

    mode = sys.argv[1]
    directory = sys.argv[2]

    if not os.path.exists(directory):
        print("[-] Directory does not exist.")
        return

    if mode == "init":
        create_baseline(directory)
    elif mode == "check":
        monitor_integrity(directory)
    else:
        print("[-] Invalid mode. Use 'init' or 'check'.")

if __name__ == "__main__":
    main()
