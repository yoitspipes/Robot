from pywinauto.application import Application, timings
from pywinauto.findwindows import ElementNotFoundError
import os
import subprocess
import time

def run_installer(installer_path):
	path = installer_path
	# Need to set these flags for detaching process because installer extracts contents to run a separate installer i.e. Updater.exe
	flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW

	#Note b/c of aforementioned the script will not wait for install to complete
	try:
		command = [path]
		print(f"Attempting to run: {' '.join(command)}")

		process = subprocess.Popen(command, creationflags=flags)

		# PID may be useful in the future, consider returning it
		print(f"Installer process started with PID: {process.pid}")
	
	except FileNotFoundError:
		print(f"Error: installer not found at {path}")
		return None
	except Exception as e:
		print(f"An unexpected error occurred: {e}")
		return None


def wait_for_dialog(title, timeout, retry_interval):
	app = Application()
	start_time = time.time()

	while time.time() - start_time < timeout:
		try:
			app.connect(title=title)
			return app
		except ElementNotFoundError:
			time.sleep(retry_interval)

def installer_ok():
	#Going to wait a max of 7 minutes for install complete dialog, and retry every 5 seconds throughout
    app = wait_for_dialog("Mediasite Recorder Express", 420, 5)
    dlg = app.window(title="Mediasite Recorder Express")
    dlg.wait("ready", timeout=30)
    dlg.set_focus()
    dlg.OK.click_input()


def main():
	run_installer(r"C:\\Users\\mediasite\\Desktop\\Latest\\RecorderExpress_8.19.5.exe")
	installer_ok()

if __name__ == "__main__":
	main()