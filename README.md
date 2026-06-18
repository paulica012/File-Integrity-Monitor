# File Integrity Monitor

A lightweight cybersecurity utility built in Python that monitors a specified directory and detects unauthorized file modifications, additions, or deletions. 

This project was developed to demonstrate fundamental concepts of defensive security and file system monitoring.

## Features
* **Baseline Generation:** Creates an initial snapshot (`baseline.json`) of the target directory, calculating cryptographic hashes for all files.
* **Integrity Checking:** Compares the current state of the directory against the baseline to detect altered content.
* **Alerting:** Outputs clear, color-coded console alerts for modified `[MODIFICAT]`, new `[NOU]`, or deleted `[STERS]` files.

## Technologies Used
* **Language:** Python 3
* **Libraries:** `hashlib` (SHA-256 for secure cryptographic hashing), `os`, `json`

## How to Run

1. Clone the repository to your local machine:
```bash
   git clone [https://github.com/paulica012/File-Integrity-Monitor.git](https://github.com/paulica012/File-Integrity-Monitor.git)
   ```
2. Navigate to the project directory and run the main script:
```bash
   python main.py
   ```
3. **First run:** The script will create a `test_folder` with a dummy file and generate the `baseline.json`.
4. **Subsequent runs:** Alter the file inside `test_folder` and run the script again to see the tamper detection in action.