import cv2
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog
import threading
import subprocess
import platform
from scipy.interpolate import griddata

root = tk.Tk()
root.title("Wi-Fi Mapper")
canvas = tk.Canvas(root, bg="white")
canvas.pack(side="top", fill="both", expand=True)
ctrl_frame = tk.Frame(root)
ctrl_frame.pack(side="bottom", fill="x")

load_btn = tk.Button(ctrl_frame, text="Load Floor Plan")
load_btn.pack(side="left", padx=6, pady=6)
spacing_slider = tk.Scale(ctrl_frame, from_=20, to=120, orient="horizontal", label="Spacing (px)")
spacing_slider.set(60)
spacing_slider.pack(side="left", padx=6)
heatmap_btn = tk.Button(ctrl_frame, text="Generate Heatmap")
heatmap_btn.pack(side="left", padx=6, pady=6)

max_w, max_h = 960, 540
tk_img = None
img_resized = None
mask_resized = None
gray_resized = None
dots_map = {}
tk_heatmap_img = None


def measure_wifi_once():
    try:
        system = platform.system().lower()
        if system == "windows":
            result = subprocess.check_output("netsh wlan show interfaces", shell=True).decode(errors="ignore")
            for line in result.split("\n"):
                if "Signal" in line:
                    return int(line.split(":")[1].replace("%", "").strip())
        elif system == "linux":
            result = subprocess.check_output("nmcli -t -f active,ssid,signal dev wifi", shell=True).decode(errors="ignore")
            for line in result.split("\n"):
                if line.startswith("yes:"):
                    return int(line.split(":")[-1])
        elif system == "darwin":
            result = subprocess.check_output(
                ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"]
            ).decode(errors="ignore")
            rssi, noise = None, None
            for line in result.split("\n"):
                if "agrCtlRSSI" in line:
                    rssi = int(line.split(":")[1].strip())
                if "agrCtlNoise" in line:
                    noise = int(line.split(":")[1].strip())
            if rssi is not None:
                return max(0, min(100, 2 * (rssi + 100)))
        return None
    except Exception as e:
        print("Wi-Fi strength check failed:", e)
        return None


def generate_heatmap():
    global tk_heatmap_img
    if img_resized is None or mask_resized is None:
        return
    points, values = [], []
    for info in dots_map.values():
        if info["value"] is not None:
            points.append((info["x"], info["y"]))
            values.append(info["value"])
    if len(points) < 3:
        print("Not enough data points to generate a heatmap. Please measure at least 3 points.")
        return
    points = np.array(points)
    values = np.array(values)
    h, w, _ = img_resized.shape
    grid_x, grid_y = np.mgrid[0:w, 0:h]
    try:
        grid_z = griddata(points, values, (grid_x, grid_y), method='cubic', fill_value=np.mean(values))
        grid_z = grid_z.T
    except Exception as e:
        print(f"Could not generate heatmap. Error: {e}")
        return
    min_val, max_val = 0, 100
    grid_z_normalized = np.clip((grid_z - min_val) / (max_val - min_val) * 255, 0, 255).astype(np.uint8)
    heatmap = cv2.applyColorMap(grid_z_normalized, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(img_resized, 0.6, heatmap, 0.4, 0)
    final_image = img_resized.copy()
    final_image[mask_resized == 255] = overlay[mask_resized == 255]
    pil_img = Image.fromarray(cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB))
    tk_heatmap_img = ImageTk.PhotoImage(pil_img)
    canvas.delete("heatmap")
    canvas.create_image(0, 0, anchor="nw", image=tk_heatmap_img, tags=("heatmap",))
    canvas.heatmap_ref = tk_heatmap_img
    scale_h = h
    scale_w = 40
    gradient = np.linspace(0, 255, scale_h, dtype=np.uint8).reshape(-1, 1)
    scale_img = cv2.applyColorMap(gradient, cv2.COLORMAP_JET)
    scale_pil = Image.fromarray(cv2.cvtColor(scale_img, cv2.COLOR_BGR2RGB))
    scale_draw = ImageDraw.Draw(scale_pil)
    font = ImageFont.load_default()
    for val in [0, 20, 40, 60, 80, 100]:
        y = int(scale_h - (val / 100.0) * scale_h)
        scale_draw.text((scale_w + 5, y), f"{val}%", fill="black", font=font)
    tk_scale_img = ImageTk.PhotoImage(scale_pil)
    canvas.create_image(w + 10, 0, anchor="nw", image=tk_scale_img, tags=("heatmap",))
    canvas.scale_img_ref = tk_scale_img


def on_dot_click(dot_id):
    if dot_id not in dots_map:
        return
    if dots_map[dot_id]["measured"]:
        return
    dots_map[dot_id]["measured"] = True
    canvas.itemconfig(dot_id, fill="purple")
    x, y = dots_map[dot_id]["x"], dots_map[dot_id]["y"]
    t = threading.Thread(target=_measure_thread, args=(dot_id, x, y), daemon=True)
    t.start()


def _measure_thread(dot_id, x, y):
    val = measure_wifi_once()
    strength_text = f"{val}%" if val is not None else "N/A"
    print(f"Dot clicked at: ({x}, {y}), Wi-Fi Strength: {strength_text}")
    dots_map[dot_id]["value"] = val

    def ui_update():
        txt = f"{val}%" if val is not None else "n/a"
        label_id = canvas.create_text(x + 10, y, text=txt, anchor="w", font=("TkDefaultFont", 9),
                                      fill="black", tags=("dotlabel",))
        dots_map[dot_id]["label"] = label_id

    root.after(0, ui_update)


def place_dots():
    canvas.delete("dot")
    canvas.delete("dotlabel")
    canvas.delete("heatmap")
    canvas.update_idletasks()
    if img_resized is None or mask_resized is None or gray_resized is None:
        return
    spacing = int(spacing_slider.get())
    h, w = mask_resized.shape
    r = max(3, spacing // 20)
    for y in range(r, h, spacing):
        for x in range(r, w, spacing):
            if mask_resized[y, x] == 255 and int(gray_resized[y, x]) > 200:
                dot = canvas.create_oval(x - r, y - r, x + r, y + r, fill="red", outline="", tags=("dot",))
                dots_map[dot] = {"x": x, "y": y, "measured": False, "value": None, "label": None}
                canvas.tag_bind(dot, "<Button-1>", lambda e, d=dot: on_dot_click(d))


def load_and_process_image():
    global tk_img, img_resized, mask_resized, gray_resized, dots_map
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if not path:
        return
    color = cv2.imread(path)
    gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    inv = cv2.bitwise_not(thresh)
    kernel = np.ones((5, 5), np.uint8)
    closed = cv2.morphologyEx(inv, cv2.MORPH_CLOSE, kernel, iterations=2)
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return
    largest = max(contours, key=cv2.contourArea)
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [largest], -1, 255, -1)
    h, w = gray.shape
    scale = min(max_w / w, max_h / h, 1.0)
    new_w, new_h = int(w * scale), int(h * scale)
    img_resized = cv2.resize(color, (new_w, new_h), interpolation=cv2.INTER_AREA)
    mask_resized = cv2.resize(mask, (new_w, new_h), interpolation=cv2.INTER_NEAREST)
    gray_resized = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    pil_img = Image.fromarray(cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB))
    tk_img = ImageTk.PhotoImage(pil_img)
    canvas.config(width=new_w + 70, height=new_h)
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=tk_img, tags=("bg",))
    dots_map = {}
    place_dots()


def refresh_dots(event=None):
    place_dots()


load_btn.config(command=load_and_process_image)
spacing_slider.bind("<ButtonRelease-1>", refresh_dots)
heatmap_btn.config(command=generate_heatmap)

root.mainloop()
