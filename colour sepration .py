import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

class ColorSeparationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Separation App")

        # UI elements
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.generate_button = tk.Button(root, text="Generate Color Images", command=self.generate_color_images)
        self.generate_button.pack()

        self.colors_var = tk.StringVar()
        self.colors_entry = tk.Entry(root, textvariable=self.colors_var, width=20)
        self.colors_entry.pack()

        self.status_label = tk.Label(root, text="")
        self.status_label.pack()

        # Image variables
        self.original_image = None
        self.color_images = []

    def load_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.display_image()

    def display_image(self):
        if self.original_image:
            image_tk = ImageTk.PhotoImage(self.original_image)
            self.canvas.config(width=image_tk.width(), height=image_tk.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
            self.canvas.image_tk = image_tk

    def generate_color_images(self):
        colors_str = self.colors_var.get()
        try:
            colors = [tuple(map(int, c.split(','))) for c in colors_str.split(';')]
            self.color_images = self.separate_colors(colors)
            self.display_color_images()
            self.status_label.config(text="Color images generated successfully.")
        except ValueError:
            self.status_label.config(text="Invalid color format. Use R,G,B;R,G,B;...")

    def separate_colors(self, colors):
        color_images = []
        original_array = np.array(self.original_image)
        for color in colors:
            mask = np.all(original_array == color, axis=-1)
            color_image = np.zeros_like(original_array)
            color_image[mask] = original_array[mask]
            color_images.append(Image.fromarray(color_image))
        return color_images

    def display_color_images(self):
        for i, color_image in enumerate(self.color_images):
            color_image_tk = ImageTk.PhotoImage(color_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=color_image_tk)
            self.canvas.image_tk = color_image_tk
            color_image.save(f"color_image_{i + 1}.png")  # Save color image to file

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorSeparationApp(root)
    root.mainloop()
