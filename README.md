# File Change Tracker

A desktop application that monitors file changes in specified folders (Desktop and Downloads by default), automatically creates **backups**, **encrypts** modified files using AES encryption, and deletes the original files for added security. The app also features **user authentication** to securely decrypt files.

## Features

- Real-time monitoring of Desktop and Downloads folders
- On file modification:
  - Creates an encrypted backup
  - Encrypts the file using AES
  - Deletes the original file to protect data
- User-friendly GUI with:
  - File decryption (requires user login)
  - User registration system

## Supported File Types

Supports common file types including `.pdf`, `.jpg`, `.png`, `.mp4`, `.mp3`, `.docx`, `.xlsx`, `.pptx`, `.txt`, `.rtf`, and more.

## Requirements

- Python 3.7 or newer
- Required Python packages:
  - `cryptography`
  - `watchdog`
  - `tkinter` (bundled with Python)

## Installation & Usage

1. Clone the repository:
    ```bash
    git clone https://github.com/Hacerrr5/Encrypted-File-Backup-Change-Tracker.git
    cd Encrypted-File-Backup-Change-Tracker
    ```

2. Install dependencies:
    ```bash
    pip install cryptography watchdog
    ```

3. Run the application:
    ```bash
    python app.py
    ```

## Interface Overview

- **Start:** Begin monitoring the selected folders for file changes.
- **Stop:** Stop monitoring.
- **Decrypt File:** Select and decrypt files (requires authentication).
- **Add User:** Register a new user (needed for decryption).

## Security

Backups and encrypted files use AES encryption via the `cryptography` library. Only authenticated users can decrypt files, ensuring data safety.

## Developer

Developed by [Hacer](https://github.com/Hacerrr5).

## License

This project is licensed under the MIT License.

---


