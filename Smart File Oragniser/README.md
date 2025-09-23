# Smart File Organiser

This is a simple yet powerful Python script that automatically organizes files in a specified folder into categorized subdirectories based on their file type. It's the perfect solution for tidying up cluttered download folders or any other messy directory.

### Features

* **Automated Sorting**: Sorts files into predefined folders like "Images," "Docs," "Videos," and "Music."
* **Intelligent Handling**: Automatically creates the necessary destination folders if they don't already exist.
* **User-Friendly**: Provides clear output to show which files are being moved and where.
* **Customizable**: Easily expandable to sort more file types and create new categories.

### Prerequisites

* **Python 3.x**: The script is written in Python 3 and uses only built-in libraries, so no additional installations are required.

### How to Run

1.  **Save the Script**: Save the Python code as a file named `organiser.py`.
2.  **Open a Terminal**: Open your command prompt (Windows) or terminal (macOS/Linux).
3.  **Navigate to the Script's Location**: Use the `cd` command to go to the directory where you saved the `organiser.py` file.
4.  **Run the Script**: Execute the script using the following command:

    ```bash
    python organiser.py
    ```

5.  **Provide the Folder Path**: The script will prompt you to "Drop the folder path here." You can either:
    * Manually type or paste the full path to the folder you want to organize.
    * Drag and drop the folder directly into the terminal window. (This method works on most operating systems and automatically pastes the full path for you.)

**Before Running the Script:**
my-messy-folder/
├── photo1.jpg
├── report.pdf
├── song.mp3
├── video.mp4
├── another-file.zip
├── photo2.jpeg
└── document.docx

**After Running the Script:**

my-messy-folder/
├── Images/
│   ├── photo1.jpg
│   └── photo2.jpeg
├── Docs/
│   ├── report.pdf
│   └── document.docx
├── Videos/
│   └── video.mp4
├── Music/
│   └── song.mp3
└── another-file.zip


### Customization

You can easily customize the script to sort different file types or add new categories. Edit the `file` and `exts` lists at the beginning of the `organiser.py` file.

**Example**: To add a "Compressed" folder for `.zip` and `.rar` files, modify the lists as follows:

```python
file = ["Images", "Docs", "Videos", "Music", "Compressed"]
exts = [[".jpg", ".png", ".jpeg"], [".pdf", ".docx"], [".mp4"], [".mp3"], [".zip", ".rar"]]
Note
The script is designed to ignore any existing subfolders within the target directory. Files with extensions not defined in the exts list will remain in their original location.

