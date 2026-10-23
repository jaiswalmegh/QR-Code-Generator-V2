
# ✦ QR NOVA | Creative QR Studio

A modern desktop QR code generator built with Python, CustomTkinter, qrcode, and Pillow.

## Features

- Text and website URL QR codes
- Wi-Fi QR codes with security and hidden-network settings
- vCard contact QR codes
- Custom foreground and background colors
- Adjustable QR quiet-zone border
- Four error-correction levels
- PNG and JPEG export
- Multiple export resolutions: 512, 1024, and 2048 pixels
- Dark-themed interface with QR preview
- Local generation without external APIs

## Tech Stack

- Python
- CustomTkinter
- qrcode
- Pillow
- Tkinter

## Installation

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Application

```bash
python main.py
```

## Project Structure

```text
QR-NOVA/
├── main.py
├── requirements.txt
└── README.md
```

## How to Use

1. Select a content type.
2. Enter the text, URL, Wi-Fi credentials, or contact information.
3. Customize colors, border size, and error correction.
4. Select the output resolution and image format.
5. Click Generate QR.
6. Save your QR code as a PNG or JPEG image.

## Design Notes

Use a high-contrast foreground and background for reliable scanning. Always test generated QR codes with a phone before distributing them.

Wi-Fi QR compatibility may vary between devices. Do not publicly share QR codes containing private network credentials.

## Privacy

QR codes are generated locally. No account or external API is required.

## Author

Megh Jaiswal
