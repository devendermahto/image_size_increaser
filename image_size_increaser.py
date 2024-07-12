import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def increase_image_size(file_path, min_size_mb=2, max_size_mb=5):
    with open(file_path, 'rb') as f:
        image_data = f.read()

    # Create a large metadata string to increase file size
    metadata = str_repeat("metadata1234567890", 50000)
    new_image_data = image_data + metadata.encode()

    output_path = os.path.splitext(file_path)[0] + "IMG" + os.path.splitext(file_path)[1]
    with open(output_path, 'wb') as f:
        f.write(new_image_data)

    while os.path.getsize(output_path) < min_size_mb * 1024 * 1024:
        with open(output_path, 'ab') as f:
            f.write(str_repeat("metadata1234567890", 1000).encode())

    while os.path.getsize(output_path) > max_size_mb * 1024 * 1024:
        with open(output_path, 'rb') as f:
            new_image_data = f.read()

        new_image_data = new_image_data[:-1000]
        with open(output_path, 'wb') as f:
            f.write(new_image_data)

    return output_path

def str_repeat(string, times):
    return string * times

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if not file_path:
        return

    processed_image_path = increase_image_size(file_path)
    display_image(processed_image_path)

def display_image(image_path):
    preview_window = tk.Toplevel(root)
    preview_window.title("Preview Processed Image")
    preview_window.geometry("400x400")

    img = Image.open(image_path)
    img.thumbnail((400, 400))
    img = ImageTk.PhotoImage(img)

    panel = tk.Label(preview_window, image=img)
    panel.image = img
    panel.pack()

    save_button = tk.Button(preview_window, text="Save Image", command=lambda: save_image(image_path))
    save_button.pack(pady=10)

def save_image(image_path):
    save_dir = filedialog.askdirectory()
    if save_dir:
        save_path = os.path.join(save_dir, os.path.basename(image_path))
        os.rename(image_path, save_path)
        messagebox.showinfo("Image Saved", f"Image saved to {save_path}")

root = tk.Tk()
root.title("Image Size Increaser")
root.geometry("300x200")

upload_button = tk.Button(root, text="Upload Image", command=open_image)
upload_button.pack(expand=True)

root.mainloop()
