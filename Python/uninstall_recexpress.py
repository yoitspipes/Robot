import time
import sys
import re
import os
import ctypes
import subprocess
import winreg
import pygetwindow as gw
from pywinauto.application import Application

#This will close Recorder Express UI if it is open, otherwise proceeds
def close_express_window(partial_title, case_insensitive=True):

    def match(title):
        return partial_title.lower() in title.lower() if case_insensitive else partial_title in title

    # Find matching windows
    windows = [w for w in gw.getAllWindows() if match(w.title)]

    if not windows:
        print(f"No windows found with title containing '{partial_title}'")
        return

    for win in windows:
        try:
            app = Application().connect(handle=win._hWnd)
            print(f"Closing window: {win.title}")
            app.window(handle=win._hWnd).close()
        except Exception as e:
            print(f"Failed to close '{win.title}': {e}")

#PowerShell scripts called below to shut down Recorder Express processes prior to uninstall, and delete leftover directories post-uninstall
#TODO - Consider using psutil
def terminator(powshell_script_path):
    result = subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", powshell_script_path],
    capture_output=True,
    text=True)

def installer_dialog():
    time.sleep(1)
    app = Application(backend="win32").connect(title="Windows Installer")
    dlg = app.window(title="Windows Installer", control_type="Window")
    dlg.Yes.click_input()


APP_NAME = "Mediasite Recorder"  #As displayed in Programs & Features

def is_admin():
   """Check if running with admin privileges"""
   try:
       return ctypes.windll.shell32.IsUserAnAdmin()
   except:
       return False
def get_uninstall_command(app_name):
   """Search registry uninstall keys for the app's uninstall command"""
   reg_paths = [r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall", r"SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall",]
   for reg_path in reg_paths:
       try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
               for i in range(0, winreg.QueryInfoKey(key)[0]):
                   try:
                       subkey_name = winreg.EnumKey(key, i)
                       with winreg.OpenKey(key, subkey_name) as subkey:
                           display_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                           if app_name.lower() in display_name.lower():
                               uninstall_cmd, _ = winreg.QueryValueEx(subkey, "UninstallString")
                               return uninstall_cmd
                   except FileNotFoundError:
                       continue
                   except OSError:
                       continue
       except FileNotFoundError:
           continue
   return None

def normalize_uninstall_command(uninstall_cmd):
   """Attempt silent mode uninstall if possible"""
   if not uninstall_cmd:
       return None
   # Handle MSI uninstallers
   if "MsiExec.exe" in uninstall_cmd or "msiexec.exe" in uninstall_cmd.lower():
       match = re.search(r"\{[0-9A-F-]+\}", uninstall_cmd, re.IGNORECASE)
       if match:
           product_code = match.group(0)
           return f'msiexec /x {product_code} /quiet /norestart'
   # Handle EXE uninstallers - try adding common silent flags
   if uninstall_cmd.lower().endswith(".exe") or ".exe" in uninstall_cmd.lower():
       return f'"{uninstall_cmd}" /S /quiet /norestart'
   return uninstall_cmd


def uninstall_recorder():
   if not is_admin():
       # Relaunch as admin
       ctypes.windll.shell32.ShellExecuteW(
           None, "runas", sys.executable, " ".join(sys.argv), None, 1
       )
       sys.exit()
   uninstall_cmd = get_uninstall_command(APP_NAME)
   if not uninstall_cmd:
       print(f"Uninstall command not found for '{APP_NAME}'")
       sys.exit(1)
   print(f"Original uninstall command: {uninstall_cmd}")
   uninstall_cmd = normalize_uninstall_command(uninstall_cmd)
   print(f"Normalized uninstall command: {uninstall_cmd}")
   try:
       subprocess.run(uninstall_cmd, shell=True, check=True)
       print(f"Successfully uninstalled {APP_NAME}")
   except subprocess.CalledProcessError as e:
       print(f"Uninstall failed: {e}")

def disable_iis():
   try:
       cmd = 'dism /Online /Disable-Feature /FeatureName:IIS-WebServerRole /NoRestart'
       subprocess.run(cmd, shell=True, check=True)
       print("IIS feature disabled successfully - proceeding with reboot.")
   except subprocess.CalledProcessError as e:
        #TODO - figure out why this except is raised despite success
       print(f"Failed to disable IIS: {e}")

def reboot():
    print("Rebooting PC in 10 seconds.")
    os.system("shutdown -t 10 -r -f")

def main():
    close_express_window("Mediasite Recorder Express")
    print()
    terminator(r"C:\\Users\\mediasite\\Desktop\\Python\\terminate_express_process.ps1")
    print("Recorder processes successfully terminated.")
    print() #inserting blank row for better readability
    uninstall_recorder()
    print()
    terminator(r"C:\\Users\\mediasite\\Desktop\\Python\\remove_recorder_directories.ps1")
    print("Recorder Express directories have been removed.")
    print()
    disable_iis()
    print()
    reboot()

if __name__ == "__main__":
    main()