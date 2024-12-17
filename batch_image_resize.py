import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from PIL import Image
import os
from pathlib import Path


class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Resizer")
        self.root.geometry("685x500")
        self.root.tk.call('tk', 'scaling', 2.0)  # Improve scaling/resolution

        # Make the window responsive
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Update main_frame:
        main_frame = ttk.Frame(root, padding="20", style='Modern.TFrame')
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)

        # Configure modern style
        self.style = ttk.Style()
        if os.name == 'nt':  # Windows
            self.style.theme_use('vista')
        else:  # macOS and Linux
            self.style.theme_use('clam')

        # Modify font configurations:
        default_font = ('Segoe UI', 10)  # Windows
        if os.name != 'nt':  # macOS/Linux
            default_font = ('SF Pro Text', 10)

        self.style.configure('Modern.TFrame', background='#f0f0f0')
        self.style.configure('Modern.TButton', padding=5, font=default_font)
        self.style.configure('Modern.TLabel', font=default_font, background='#f0f0f0')

        # Configure colors and styles
        self.style.configure('Modern.TFrame', background='#f0f0f0')
        self.style.configure('Modern.TButton',
                             padding=5,
                             font=('Helvetica', 10))
        self.style.configure('Modern.TLabel',
                             font=('Helvetica', 10),
                             background='#f0f0f0')
        self.style.configure('Horizontal.TProgressbar',
                             background='#2196f3',
                             troughcolor='#e0e0e0')

        # Create main frame with padding and style
        main_frame = ttk.Frame(root, padding="20", style='Modern.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Folder selection
        folder_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        folder_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(folder_frame,
                  text="Select Folder:",
                  style='Modern.TLabel').grid(row=0, column=0, sticky=tk.W)

        self.folder_path = tk.StringVar()
        folder_entry = ttk.Entry(folder_frame,
                                 textvariable=self.folder_path,
                                 width=50)
        folder_entry.grid(row=0, column=1, padx=5)

        browse_btn = ttk.Button(folder_frame,
                                text="Browse",
                                command=self.browse_folder,
                                style='Modern.TButton')
        browse_btn.grid(row=0, column=2, padx=(5, 0))

        # Resize percentage
        resize_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        resize_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))

        ttk.Label(resize_frame,
                  text="Resize Percentage (1-100):",
                  style='Modern.TLabel').grid(row=0, column=0, sticky=tk.W)

        self.resize_percentage = tk.StringVar(value="50")
        ttk.Entry(resize_frame,
                  textvariable=self.resize_percentage,
                  width=10).grid(row=0, column=1, sticky=tk.W, padx=5)

        # Process button
        ttk.Button(main_frame,
                   text="Process Images",
                   command=self.process_images,
                   style='Modern.TButton').grid(row=2, column=0, columnspan=3, pady=(0, 15))

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame,
                                            variable=self.progress_var,
                                            maximum=100,
                                            style='Horizontal.TProgressbar')
        self.progress_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))

        # Log area
        log_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.rowconfigure(4, weight=1)

        self.log_area = scrolledtext.ScrolledText(
            log_frame,
            width=70,
            height=15,
            font=('SF Mono' if os.name != 'nt' else 'Consolas', 9),
            background='#ffffff',
            foreground='#333333'
        )
        self.log_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)

    def log_message(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.root.update()

    def process_images(self):
        folder = self.folder_path.get()
        try:
            resize_percent = float(self.resize_percentage.get())
            if not 1 <= resize_percent <= 100:
                raise ValueError("Percentage must be between 1 and 100")
        except ValueError as e:
            self.log_message(f"Error: {str(e)}")
            return

        if not folder:
            self.log_message("Please select a folder first.")
            return

        # Create resized subdirectory
        output_dir = Path(folder) / 'resized'
        output_dir.mkdir(exist_ok=True)

        # Get list of images
        image_files = []
        for ext in ('.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG'):
            image_files.extend(Path(folder).glob(f"*{ext}"))

        if not image_files:
            self.log_message("No images found in the selected folder.")
            return

        # Clear log area
        self.log_area.delete(1.0, tk.END)

        # Process images
        scale_factor = resize_percent / 100
        total_files = len(image_files)

        for i, image_path in enumerate(image_files, 1):
            try:
                # Open image
                with Image.open(image_path) as img:
                    # Calculate new size
                    new_width = int(img.width * scale_factor)
                    new_height = int(img.height * scale_factor)

                    # Resize image with high quality
                    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                    # Create output filename (same name in resized directory)
                    output_path = output_dir / image_path.name

                    # Save with high quality
                    if image_path.suffix.lower() in ('.jpg', '.jpeg'):
                        resized_img.save(output_path, 'JPEG', quality=95)
                    else:  # PNG
                        resized_img.save(output_path, 'PNG', optimize=True)

                    self.log_message(f"Processed: {image_path.name}")

            except Exception as e:
                self.log_message(f"Error processing {image_path.name}: {str(e)}")

            # Update progress bar
            progress = (i / total_files) * 100
            self.progress_var.set(progress)
            self.root.update()

        self.log_message(f"\nProcessing complete! Resized images saved in: {output_dir}")
        self.progress_var.set(100)


def main():
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
