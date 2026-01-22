import hashlib
import json
import os
from datetime import datetime

DATA_FILE = "integrity_hashes.json"

class IntegrityChecker:
    def __init__(self):
        self.tracked_files = self.load_tracked_files()

    def load_tracked_files(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                    return data.get("tracked_files", {})
            except:
                print("Error loading hash database. Starting fresh.")
                return {}
        return {}

    def save_tracked_files(self):
        data = {"tracked_files": self.tracked_files}
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print("Hash database updated successfully.")

    def compute_hash(self, file_path):
        if not os.path.exists(file_path):
            return None, "File not found"
        if not os.access(file_path, os.R_OK):
            return None, "Permission denied"
        
        sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            return sha256.hexdigest(), None
        except Exception as e:
            return None, f"Error reading file: {str(e)}"

    def add_file(self):
        file_path = input("\nEnter full path to file to track: ").strip()
        file_path = os.path.normpath(file_path)
        
        if not os.path.exists(file_path):
            print("File does not exist.")
            return
        
        current_hash, error = self.compute_hash(file_path)
        if error:
            print(error)
            return
        
        self.tracked_files[file_path] = current_hash
        self.save_tracked_files()
        print(f"File added and hash stored successfully.")
        print(f"SHA-256: {current_hash}")

    def verify_file(self):
        file_path = input("\nEnter full path to file to verify: ").strip()
        file_path = os.path.normpath(file_path)
        
        if file_path not in self.tracked_files:
            print("File not tracked. Add it first.")
            return
        
        current_hash, error = self.compute_hash(file_path)
        if error:
            print(error)
            return
        
        stored_hash = self.tracked_files[file_path]
        
        print(f"\nVerification Result for: {file_path}")
        print(f"Stored SHA-256:  {stored_hash}")
        print(f"Current SHA-256: {current_hash}")
        
        if current_hash == stored_hash:
            print("→ INTEGRITY VERIFIED (File unchanged)")
        else:
            print("!!! INTEGRITY COMPROMISED !!!")
            print("File has been modified or corrupted!")

    def verify_all_files(self):
        if not self.tracked_files:
            print("No files are being tracked.")
            return
        
        print("\nVerifying all tracked files...")
        print("-" * 70)
        for file_path, stored_hash in self.tracked_files.items():
            current_hash, error = self.compute_hash(file_path)
            status = "OK" if not error and current_hash == stored_hash else "FAILED"
            print(f"{status:<8} | {file_path}")
        print("-" * 70)

    def list_tracked_files(self):
        if not self.tracked_files:
            print("No files are being tracked.")
            return
        print("\nTracked Files:")
        for i, path in enumerate(self.tracked_files.keys(), 1):
            print(f"{i:3d}. {path}")

    def remove_file(self):
        self.list_tracked_files()
        try:
            index = int(input("\nEnter number of file to remove: ")) - 1
            path = list(self.tracked_files.keys())[index]
            del self.tracked_files[path]
            self.save_tracked_files()
            print(f"File removed from tracking: {path}")
        except:
            print("Invalid selection.")

    def display_menu(self):
        print("\n" + "="*60)
        print("     FILE INTEGRITY CHECKER & HASH VERIFIER")
        print("="*60)
        print("1. Add file to track (compute & store hash)")
        print("2. Verify a single file")
        print("3. Verify all tracked files")
        print("4. List all tracked files")
        print("5. Remove file from tracking")
        print("6. Exit & Save")
        print("="*60)

    def run(self):
        print("File Integrity Checker – Cybersecurity Tool\n")
        while True:
            self.display_menu()
            choice = input("Choose (1-6): ").strip()
            
            if choice == "1":
                self.add_file()
            elif choice == "2":
                self.verify_file()
            elif choice == "3":
                self.verify_all_files()
            elif choice == "4":
                self.list_tracked_files()
            elif choice == "5":
                self.remove_file()
            elif choice == "6":
                self.save_tracked_files()
                print("Goodbye! Stay secure.")
                break
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    checker = IntegrityChecker()
    checker.run()
