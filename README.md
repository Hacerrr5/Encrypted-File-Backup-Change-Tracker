# File Change Tracker

This is a desktop application that monitors file changes in specific folders (Desktop and Downloads by default), creates a **backup**, **encrypts** the changed file, and deletes the original file. It also supports **user authentication** for secure decryption.

## Features

- Real-time monitoring of Desktop and Downloads folders
- On file modification:
  - Creates a backup
  - Encrypts the file using AES
  - Deletes the original file
- GUI interface with:
  - File decryption (with user login)
  - User registration

## Usage

1. Clone or download the project:
    ```bash
    git clone https://github.com/yourusername/project-name.git
    cd project-name
    ```

2. Install required Python modules:
    ```bash
    pip install cryptography watchdog
    ```

3. Run the application:
    ```bash
    python app.py
    ```

## Interface Overview

- **Start:** Begin monitoring changes in selected directories.
- **Stop:** Stop monitoring.
- **Decrypt File:** Select and decrypt a file (authentication required).
- **Add User:** Add a new user account (required for decryption).

## Supported File Types

Includes: `.pdf`, `.jpg`, `.png`, `.mp4`, `.mp3`, `.docx`, `.xlsx`, `.pptx`, `.txt`, `.rtf`, and more.

## Requirements

- Python 3.7 or newer
- `cryptography`, `watchdog`, `tkinter` (Tkinter is bundled with Python)

## Security

All backups are AES-encrypted using the `cryptography` library. Files can only be decrypted with valid username and password credentials.

## Developer

Developed by [Hacer](https://github.com/yourusername).

## License

This project is licensed under the MIT License.

---

💡 Looking for Turkish GPT-powered tools and resources? Visit [https://gptonline.ai/tr/](https://gptonline.ai/tr/)
