Name: Olorunfemi Favour Adesanmi
Matric Number: 24/14744
Course: Sen201
Department: Cyber Security

File Integrity Checker

Purpose

The File Integrity Checker is a cybersecurity tool designed to detect
unauthorized changes to files. It works by computing and storing the SHA-256
hash of selected files. At a later time, it can re-compute the hash and compare
it with the stored value to verify if the file has been modified or corrupted.

Features

- Track Files: Calculate and store the SHA-256 hash of a file.
- Verify Single File: Check if a specific file has changed since it was last
  tracked.
- Verify All Files: Batch verification of all tracked files.
- List Tracked Files: View a list of all files currently being monitored.
- Remove File: Stop tracking a specific file.
- Persistence: Hashes are saved to `integrity_hashes.json` for persistent
  tracking across sessions.

Usage

1. Run the script using Python:
   ```bash
   python "assighment2{hash-integrity-checker}.py"
   ```
2. Follow the interactive menu options:
   - Choose `1` to add a file to track (provide the full path).
   - Choose `2` to verify a specific file.
   - Choose `3` to verify all tracked files.
   - Choose `4` to list tracked files.
   - Choose `5` to remove a file from tracking.
   - Choose `6` to exit and save the database.

Requirements

- Python 3.x
- Standard libraries (no external dependencies required): `hashlib`, `json`,
  `os`, `datetime`.
