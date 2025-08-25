from pywinauto.application import Application, timings
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.findbestmatch import MatchError
from pywinauto.keyboard import send_keys
import os
import json
import time
import sys
import argparse

def wait_for_dialog(title, timeout, retry_interval):
	app = Application()
	start_time = time.time()

	while time.time() - start_time < timeout:
		try:
			app.connect(title=title)
			return app
		except ElementNotFoundError:
			time.sleep(retry_interval)
	raise ElementNotFoundError(f"Dialog '{title}' not found after {timeout} seconds.")


def import_preso(preso_name):
	app = wait_for_dialog("Select Folder", 30, 2)
	dlg = app.window(title="Select Folder")
	dlg.set_focus()

	dlg['']

	#Browser remembers last file explorer session, need to force address to default path
	docs_path = os.path.join(os.environ['USERPROFILE'], 'Documents')


	dlg['Address band Root'].click_input()
	dlg.wait("ready", timeout=5)
	send_keys(docs_path)
	send_keys('{ENTER}')
	dlg.wait("ready", timeout=5)
	time.sleep(1)

	dlg['Search'].click_input()
	send_keys(preso_name)
	dlg.wait("ready", timeout=5)
	time.sleep(1)
	dlg['DirectUIHWND0'].click_input() #TODO - find better way, this clicks on empty space
	send_keys(preso_name) #TODO cont. - this blindly sends keyboard input to make the one result active so that it can be opened

	dlg.wait("ready", timeout=5)
	time.sleep(1)

	dlg['Select Folder'].click_input()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Import a presentation folder via Windows dialog automation.")
    parser.add_argument("preso_name", help="Name of the presentation folder to import")
    args = parser.parse_args()

    try:
        import_preso(args.preso_name)
        print("import_preso completed successfully")
    except Exception as e:
        print(f"import_preso failed: {e}")
        exit(2)