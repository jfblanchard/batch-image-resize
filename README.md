# Image Resizer

A Python desktop application that batch resizes images while maintaining high quality. Features a modern GUI interface with progress tracking.

## Features

- Resize multiple images (PNG, JPG) simultaneously
- Specify resize percentage (1-100%)
- Preserves image quality (95% JPEG quality, optimized PNG)
- Progress tracking with status updates
- Saves resized images in a separate '/resized' subdirectory
- Original files remain untouched

## Requirements

- Python 3.6+
- Pillow (PIL)
- tkinter (usually comes with Python)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/image-resizer.git
cd image-resizer

# Install dependencies
pip install Pillow
```

## Usage

1. Run the application:
```bash
python image_resizer.py
```

2. Click "Browse" to select a folder containing images
3. Enter desired resize percentage (1-100)
4. Click "Process Images"
5. Resized images will be saved in a '/resized' subdirectory

## Technical Details

- Uses LANCZOS resampling for high-quality resizing
- Supports PNG and JPG/JPEG files (case insensitive)
- Maintains original file names
- Optimized for batch processing

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request