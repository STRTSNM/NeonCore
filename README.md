# NeonCore

This Python script automatically monitors removable drives (like USB drives) on a Windows system and copies files with specified extensions to a designated backup folder.

---

## Features

- **Automatic Detection**: Monitors USB drives as soon as they are plugged in or removed.
- **Selective Backup**: Copies only files with these extensions:
.pdf, .docx, .pptx, .xlsx, .doc, .ppt, .xls, .txt, .rtf

- **Versioning**: Avoids overwriting existing files by creating numbered copies if a file with the same name already exists.
- **Preserves Metadata**: Uses `shutil.copy2` to preserve file modification times.
- **Windows Compatible**: Uses `win32api`, `win32gui`, and `win32con` for drive detection.

---

## Requirements

- Python 3.x  
- `pywin32` library (for Windows-specific device monitoring)

Install dependencies using pip:

```bash
pip install pywin32
```
## Usage
Save the script to your computer and run it.
```bash
python usb_backup.py
```
The script will create a backup folder in your user directory:

`C:\Users\<YourUsername>\Prograrns`

Insert a USB drive. The script will automatically scan it and copy the target files.

It continues running and monitors for new USB drives.


## Notes
 - Designed specifically for Windows.

 - Requires administrative privileges if certain drives or folders are restricted.

 - Avoid using on system drives or critical folders to prevent accidental file copying conflicts.

## License
This project is provided as-is under the MIT License. Use responsibly.
