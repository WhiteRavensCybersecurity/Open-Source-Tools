SentinelHash 🛡️
A Lightweight File Integrity Monitor (FIM)

SentinelHash is a Python-based security tool designed to detect unauthorized changes to your file system. It creates a cryptographic fingerprint of your files and alerts you to modifications, deletions, or new file injections. It is ideal for detecting ransomware activity, web shell injections, or accidental configuration changes.

🚀 Features
Zero Dependencies: Runs on standard Python libraries (no pip install required).

SHA-256 Hashing: Uses industry-standard encryption for precise file fingerprinting.

3-Way Detection: Identifies Modified, Deleted, and New files.

Cross-Platform: Works on Windows, macOS, and Linux.

Lightweight: Efficiently handles directory scanning without heavy resource usage.

📋 Prerequisites
Python 3.x installed on your system.

To check, open your terminal and type: python --version

⚙️ Installation & Setup
Create the Script: Create a file named sentinel.py and paste the source code provided in the previous step.

Project Structure: Your folder should look like this:

Plaintext

/MySecurityProject
├── sentinel.py          # The tool script
├── README.md            # This documentation
└── /target_folder       # The folder you want to monitor
📖 How to Use
The tool operates in two modes: Init (Initialization) and Check (Monitoring).

1. Initialize the Baseline
Before monitoring, you must establish a "known good" state. This scans the target folder and saves the file hashes.

Syntax:

Bash

python sentinel.py init <directory_path>
Example:

Bash

python sentinel.py init ./my_important_docs
Result: A file named sentinel_baseline.json is created in your current directory.

2. Run the Monitor
Run this command whenever you want to check the integrity of the files.

Syntax:

Bash

python sentinel.py check <directory_path>
Example:

Bash

python sentinel.py check ./my_important_docs
📊 Interpreting the Output
When running the check mode, you will see one of the following reports:

Scenario A: System is Clean

Plaintext

--- INTEGRITY REPORT ---
[OK] No changes detected. System is clean.
Scenario B: Changes Detected

Plaintext

--- INTEGRITY REPORT ---
[!] MODIFIED: ./my_important_docs/config.txt
[!] DELETED: ./my_important_docs/old_image.png
[!] NEW FILE DETECTED: ./my_important_docs/malware.exe

[WARNING] Integrity deviations detected!
