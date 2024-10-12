import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

# Declare file_paths globally so it can be accessed by both functions
file_paths = []
backup_location = ""

# Function to select files
def select_files():
    global file_paths  # Access the global variable
    files_listbox.delete(0, tk.END)  # Clear the listbox before inserting new files

    # Open file dialog for selecting files
    file_paths = filedialog.askopenfilenames(title="Select files")
    
    # Insert selected file names (not full paths) into the listbox
    for file in file_paths:
        file_name = os.path.basename(file)  # Get only the file name
        files_listbox.insert(tk.END, file_name)

# Function to select the backup location
def select_backup_location():
    global backup_location  # Access the global variable
    backup_location = filedialog.askdirectory(title="Select Backup Location")
    if backup_location:
        backup_label.config(text=f"Backup Location: {backup_location}")
    else:
        backup_label.config(text="Backup Location: Not selected")

# Function to backup the destination folder
def backup_destination(destination_dir):
    global backup_location  # Access the global variable
    
    if not backup_location:
        messagebox.showerror("Error", "No backup location selected.")
        return False
    
    # Create a backup folder with a timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = os.path.join(backup_location, f"backup_{timestamp}")
    
    try:
        shutil.copytree(destination_dir, backup_dir)
        messagebox.showinfo("Backup", f"Backup created at: {backup_dir}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create backup: {str(e)}")
        return False
    
    return True

# Function to copy files to the specified directory
def copy_files():
    global file_paths  # Access the global variable
    destination_dir = r"C:\Program Files (x86)\Steam\steamapps\common\Combat Master\Data\StreamingAssets\Bundles"
    
    # Check if the destination directory exists
    if not os.path.exists(destination_dir):
        messagebox.showerror("Error", "Your Bundles folder should be under C:\Program Files (x86)\Steam\steamapps\common\Combat Master\Data\StreamingAssets\Bundles")
        return

    # Backup the destination directory if the checkbox is selected
    if backup_var.get():
        if not backup_destination(destination_dir):
            return

    # Get all the selected file names from the listbox
    files = files_listbox.get(0, tk.END)
    
    # Check if there are any files selected
    if not files:
        messagebox.showwarning("Warning", "No files selected.")
        return
    
    # Copy each file to the destination directory
    for i, file in enumerate(files):
        try:
            # Since we need the full path for copying, we use file_paths[i]
            file_path = file_paths[i]
            shutil.copy(file_path, destination_dir)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy {file}: {str(e)}")
            return
    
    messagebox.showinfo("Success", "All files successfully copied to your game files.")

# Create the main window
root = tk.Tk()
root.title("Combat Master File Copier")

# Create a listbox to display selected files
files_listbox = tk.Listbox(root, width=80, height=10)
files_listbox.pack(pady=10)

# Create the select files button
select_button = tk.Button(root, text="Select Files", command=select_files)
select_button.pack(pady=10)

# Create a checkbox for the backup option
backup_var = tk.BooleanVar()  # Variable to track checkbox state
backup_checkbox = tk.Checkbutton(root, text="Backup destination folder before copying", variable=backup_var)
backup_checkbox.pack(pady=10)

# Create the select backup location button
backup_button = tk.Button(root, text="Select Backup Location", command=select_backup_location)
backup_button.pack(pady=10)

# Label to display selected backup location
backup_label = tk.Label(root, text="Backup Location: Not selected")
backup_label.pack(pady=5)

# Create the copy button
copy_button = tk.Button(root, text="Start Copying", command=copy_files)
copy_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
