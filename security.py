import os
import shutil
import time
import sqlite3
from datetime import datetime
from cryptography.fernet import Fernet
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tkinter as tk
from tkinter import messagebox, filedialog

# === EASY TO CHANGE FOLDER NAMES ===
CUSTOM_BACKUP_FOLDERNAME = "mybackups"   # Change this to your desired backup folder name!
CUSTOM_LOG_FOLDERNAME = "mylogs"         # Change this to your desired log folder name!

# === DATABASE ===
DB_FILE = "users.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_user(username, password):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def check_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# === ENCRYPTION KEY ===
KEY_FILE = 'encryption.key'
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
else:
    with open(KEY_FILE, 'rb') as key_file:
        key = key_file.read()
cipher = Fernet(key)

# === FOLDER AND FILE SETTINGS ===
TARGET_DIRS = [os.path.expanduser("~\\Desktop"), os.path.expanduser("~\\Downloads")]
BACKUP_DIR = os.path.join(os.getcwd(), CUSTOM_BACKUP_FOLDERNAME)
LOG_FILE = os.path.join(os.getcwd(), CUSTOM_LOG_FOLDERNAME, 'changes.log')

FILE_EXTENSIONS = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff',
                   '.mp4', '.avi', '.mov', '.mkv', '.flv',
                   '.mp3', '.wav', '.flac', '.aac',
                   '.docx', '.doc', '.xlsx', '.xls', '.ppt', '.pptx',
                   '.txt', '.rtf']

os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
init_db()

# === ENCRYPTION AND DECRYPTION ===
def encrypt_file(file_path):
    with open(file_path, 'rb') as f:
        encrypted_data = cipher.encrypt(f.read())
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)
    print(f"File encrypted: {file_path}")

def decrypt_file(file_path):
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()
        try:
            decrypted_data = cipher.decrypt(encrypted_data)
        except Exception as e:
            print(f"Decryption error: {e}")
            return False
    with open(file_path, 'wb') as f:
        f.write(decrypted_data)
    print(f"File decrypted: {file_path}")
    return True

# === BACKUP AND DELETE ===
def backup_and_delete(file_path):
    try:
        start_time = time.time()
        file_size = os.path.getsize(file_path) / (1024 * 1024)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_path = os.path.join(BACKUP_DIR, f"{os.path.basename(file_path)}_{timestamp}")
        shutil.copy(file_path, backup_path)
        print(f"Backup created: {file_path} -> {backup_path}")

        encrypt_file(backup_path)
        os.remove(file_path)
        print(f"Original file deleted: {file_path}")

        end_time = time.time()
        duration = end_time - start_time
        print(f"Operation finished. File size: {file_size:.2f} MB, Duration: {duration:.2f} seconds")
    except Exception as e:
        print(f"Backup or delete error: {e}")

def process_modified_file(file_path):
    if any(file_path.lower().endswith(ext) for ext in FILE_EXTENSIONS):
        if os.path.exists(file_path):
            print(f"File modified and saved: {file_path}")
            backup_and_delete(file_path)
            with open(LOG_FILE, 'a') as log:
                log.write(f"Backed up and encrypted: {file_path} - {datetime.now()}\n")

# === WATCHDOG ===
class ChangeHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"New file detected: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            print(f"File modification detected: {event.src_path}")
            process_modified_file(event.src_path)

observer = None

def start_observer():
    global observer
    observer = Observer()
    event_handler = ChangeHandler()
    for target_dir in TARGET_DIRS:
        observer.schedule(event_handler, target_dir, recursive=True)
    observer.start()
    print("Monitoring file changes. Press Stop to exit.")

def stop_observer():
    global observer
    if observer is not None:
        observer.stop()
        observer.join()
        print("Monitoring stopped.")

# === ADD USER WINDOW ===
def open_add_user_window():
    add_win = tk.Toplevel()
    add_win.title("Add User")
    add_win.geometry("320x220")
    add_win.configure(bg="#222d3a")

    tk.Label(add_win, text="Add New User", font=("Helvetica", 14, "bold"), fg="#ecf0f1", bg="#222d3a").pack(pady=(20,10))

    tk.Label(add_win, text="Username:", fg="#ecf0f1", bg="#222d3a", font=("Helvetica", 11)).pack(pady=(0,2))
    username_entry = tk.Entry(add_win, font=("Helvetica", 12))
    username_entry.pack(pady=(0,10))

    tk.Label(add_win, text="Password:", fg="#ecf0f1", bg="#222d3a", font=("Helvetica", 11)).pack(pady=(0,2))
    password_entry = tk.Entry(add_win, show="*", font=("Helvetica", 12))
    password_entry.pack(pady=(0,10))

    def submit_user():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if not username or not password:
            messagebox.showwarning("Missing Information", "Username and password cannot be empty!")
            return
        if add_user(username, password):
            messagebox.showinfo("Success", "User added!")
            add_win.destroy()
        else:
            messagebox.showerror("Error", "Username already exists!")

    tk.Button(add_win, text="Save", command=submit_user, width=15, bg="#16a085", fg="#ecf0f1", font=("Helvetica", 12, "bold")).pack(pady=10)
    tk.Button(add_win, text="Close", command=add_win.destroy, width=15, bg="#c0392b", fg="#ecf0f1", font=("Helvetica", 12, "bold")).pack()

# === USER AUTHENTICATION ON DECRYPTION ===
def decrypt_selected_file():
    file_path = filedialog.askopenfilename(title="Select File to Decrypt", initialdir=BACKUP_DIR)
    if file_path:
        auth_win = tk.Toplevel()
        auth_win.title("User Authentication")
        auth_win.geometry("320x220")
        auth_win.configure(bg="#22313f")

        tk.Label(auth_win, text="Sign In to Decrypt File", font=("Helvetica", 13, "bold"), fg="#ecf0f1", bg="#22313f").pack(pady=(20,10))
        tk.Label(auth_win, text="Username:", fg="#ecf0f1", bg="#22313f", font=("Helvetica", 11)).pack(pady=(0,2))
        username_entry = tk.Entry(auth_win, font=("Helvetica", 12))
        username_entry.pack(pady=(0,10))
        tk.Label(auth_win, text="Password:", fg="#ecf0f1", bg="#22313f", font=("Helvetica", 11)).pack(pady=(0,2))
        password_entry = tk.Entry(auth_win, show="*", font=("Helvetica", 12))
        password_entry.pack(pady=(0,10))

        def try_decrypt():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            if not username or not password:
                messagebox.showwarning("Missing Information", "Username and password cannot be empty!")
                return
            if check_user(username, password):
                success = decrypt_file(file_path)
                if success:
                    messagebox.showinfo("Success", "File decrypted successfully!")
                else:
                    messagebox.showerror("Error", "Decryption failed!")
                auth_win.destroy()
            else:
                messagebox.showerror("Error", "Incorrect username or password!")

        tk.Button(auth_win, text="Decrypt", command=try_decrypt, width=15, bg="#2980b9", fg="#ecf0f1", font=("Helvetica", 12, "bold")).pack(pady=10)
        tk.Button(auth_win, text="Close", command=auth_win.destroy, width=15, bg="#c0392b", fg="#ecf0f1", font=("Helvetica", 12, "bold")).pack()

# === GUI ===
def create_gui():
    root = tk.Tk()
    root.title("File Change Tracker")
    root.geometry("340x340")
    root.configure(bg="#2c3e50")

    title_label = tk.Label(root, text="File Change Tracker", font=("Helvetica", 16, "bold"), fg="#ecf0f1", bg="#2c3e50")
    title_label.pack(pady=12)

    start_button = tk.Button(root, text="Start", command=start_observer, width=23, bg="#27ae60", fg="#ecf0f1", font=("Helvetica", 12, "bold"))
    start_button.pack(pady=8)

    stop_button = tk.Button(root, text="Stop", command=stop_observer, width=23, bg="#c0392b", fg="#ecf0f1", font=("Helvetica", 12, "bold"))
    stop_button.pack(pady=8)

    decrypt_button = tk.Button(root, text="Decrypt File", command=decrypt_selected_file, width=23, bg="#2980b9", fg="#ecf0f1", font=("Helvetica", 12, "bold"))
    decrypt_button.pack(pady=8)

    adduser_button = tk.Button(root, text="Add User", command=open_add_user_window, width=23, bg="#f39c12", fg="#ecf0f1", font=("Helvetica", 12, "bold"))
    adduser_button.pack(pady=8)

    credit_label = tk.Label(root, text="Created by Hacer", font=("Helvetica", 10), fg="#ecf0f1", bg="#2c3e50")
    credit_label.pack(pady=18)

    root.mainloop()

if __name__ == "__main__":
    create_gui()