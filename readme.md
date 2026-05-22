# GhostClick

A lightweight, fully portable autoclicker built for speed and simplicity. 

**GhostClick** runs quietly in the background with a minimal always-on-top interface, utilizing multithreading to ensure your system never freezes while clicking at high speeds. 

## Features
- Lightweight and fully portable
- Multithreaded click engine
- OLED Dark Themed Interface
- LOW CPU and Memory Usage
- Standalone `.exe` build

<details>
<summary><strong>Logs</strong></summary>

<br>

### 1st Build — 20/05/2026 • 22:26
- Status: Successful
- Output: `GhostClick.exe`
- File Size: 10.82 MB (10,821 KB)


### 2nd Build — 20/05/2026 • 22:38 || Use of UPX 5.1.1
- Status: Failed to Run, library import errors with UPX 5.1.1
- Output: `GhostClick.exe`
- File Size: 9.07 MB (9,076 KB)

### 3rd Build - 23/05/2026 • 01:05 || Dumped the use of UPX 5.1.1
- Status: Successful
- Output: `GhostClick_v1.3_OLED_Dark.exe`
- File Size: 10.81 MB (10,814 KB)

- Added OLED Dark UI
- Improved UI responsiveness
- Refined background threading behavior
- Stability improvements and cleanup


</details>


<!-- pyinstaller --onefile --noconsole --exclude-module unittest --exclude-module email --exclude-module http --exclude-module xml --exclude-module pydoc --exclude-module urllib --exclude-module html ghost_click.py -->