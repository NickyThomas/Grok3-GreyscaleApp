import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import numpy as np

class GreyscaleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Greyscale Photo Editor")
        self.root.configure(bg="#f0f0f0")  # Light grey background for theme
        
        # Variables
        self.image = None
        self.original_image = None
        self.tk_image = None
        self.max_canvas_size = 600  # Maximum canvas width/height
        
        # GUI Elements with Styling
        self.frame = tk.Frame(root, bg="#f0f0f0")
        self.frame.pack(pady=10)
        
        self.upload_button = tk.Button(self.frame, text="Upload Photo", command=self.upload_image,
                                     bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.upload_button.pack(side=tk.LEFT, padx=5)
        
        self.save_button = tk.Button(self.frame, text="Save Image", command=self.save_image,
                                   bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # Greyscale Slider
        self.grey_label = tk.Label(root, text="Greyscale: 0%", bg="#f0f0f0", font=("Arial", 10))
        self.grey_label.pack()
        self.grey_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_image,
                                  bg="#f0f0f0", troughcolor="#d9d9d9", highlightthickness=0)
        self.grey_slider.pack(pady=5)
        
        # Contrast Slider
        self.contrast_label = tk.Label(root, text="Contrast: 1.0", bg="#f0f0f0", font=("Arial", 10))
        self.contrast_label.pack()
        self.contrast_slider = tk.Scale(root, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL,
                                      command=self.update_image, bg="#f0f0f0", troughcolor="#d9d9d9",
                                      highlightthickness=0)
        self.contrast_slider.set(1.0)  # Default contrast
        self.contrast_slider.pack(pady=5)
        
        # Canvas
        self.canvas = tk.Canvas(root, bg="white", highlightthickness=1, highlightbackground="#cccccc")
        self.canvas.pack(pady=10)
    
    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            self.original_image = Image.open(file_path).convert("RGB")
            self.image = self.original_image.copy()
            self.adjust_canvas_size()
            self.update_image(None)  # Initial display
    
    def adjust_canvas_size(self):
        # Adjust canvas size dynamically based on image, up to max_canvas_size
        width, height = self.original_image.size
        aspect_ratio = width / height
        
        if width > height:
            new_width = min(width, self.max_canvas_size)
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = min(height, self.max_canvas_size)
            new_width = int(new_height * aspect_ratio)
        
        self.canvas.config(width=new_width, height=new_height)
        self.display_image(self.image)
    
    def display_image(self, img):
        # Resize image to fit canvas
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        if width > 1 and height > 1:  # Ensure canvas is initialized
            img = img.resize((width, height), Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.canvas.create_image(width // 2, height // 2, image=self.tk_image)
    
    def update_image(self, val):
        if self.original_image:
            grey_intensity = self.grey_slider.get() / 100
            contrast_factor = self.contrast_slider.get()
            
            # Update labels
            self.grey_label.config(text=f"Greyscale: {int(grey_intensity * 100)}%")
            self.contrast_label.config(text=f"Contrast: {contrast_factor:.1f}")
            
            # Convert image to numpy array for greyscale
            img_array = np.array(self.original_image)
            grey = np.dot(img_array[..., :3], [0.299, 0.587, 0.114])
            grey_array = np.stack([grey] * 3, axis=-1)
            blended = (1 - grey_intensity) * img_array + grey_intensity * grey_array
            
            # Convert back to image and apply contrast
            self.image = Image.fromarray(np.uint8(blended))
            enhancer = ImageEnhance.Contrast(self.image)
            self.image = enhancer.enhance(contrast_factor)
            
            self.display_image(self.image)
    
    def save_image(self):
        if self.image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                   filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if file_path:
                self.image.save(file_path)
                tk.messagebox.showinfo("Success", "Image saved successfully!")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = GreyscaleApp(root)
    root.mainloop()