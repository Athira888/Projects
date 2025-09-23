# Wi-Fi Mapper / Heatmap

This project is a **Wi-Fi strength mapping tool** that allows you to create a visual heatmap of Wi-Fi signal strength on a floor plan.  
It uses Python, OpenCV, Tkinter, and NumPy to measure Wi-Fi signals and generate interactive heatmaps.

---

## Features
- Load any floor plan image (PNG, JPG, JPEG, BMP).  
- Click on dots to measure Wi-Fi signal strength at specific points.  
- Automatically generate a colored heatmap overlay.  
- Interactive GUI with adjustable spacing for measurement dots.  
- Scalable to different floor plan sizes.

---

## Prerequisites

**Python 3.x** is required, along with the following libraries:

```txt
opencv-python
numpy
pillow
scipy
tkinter  # comes with Python by default

Install the libraries using pip:
pip install opencv-python numpy pillow scipy

**Files:
-wifi_mapper.py → Main Python script
-requirements.txt → List of dependencies
- Sample floor plan images to test the heatmap

**Example folder structure:
wifi-heatmap/
│── wifi_mapper.py
│── requirements.txt
│── sample_floorplan.png
│── README.md

**USAGE**

-Run the script:

python wifi_mapper.py

-Click "Load Floor Plan" and select your floor plan image.

-Use the spacing slider to adjust the distance between measurement dots.

-Click on red dots to measure Wi-Fi signal strength at each point.

-Click "Generate Heatmap" to create the heatmap overlay on your floor plan.

-The heatmap uses a color gradient to show Wi-Fi strength: blue = weak, red = strong.

NOTES:
Works on Windows, Linux, and macOS.

Wi-Fi measurement is OS-specific:

-Windows: uses netsh wlan show interfaces

-Linux: uses nmcli

-macOS: uses the airport command-line tool

Ensure you have the necessary permissions to run these commands


