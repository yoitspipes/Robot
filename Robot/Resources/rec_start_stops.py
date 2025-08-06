from rec_runner import *

launch_recorder_web(rec_name)

preview_box = wait.until(EC.visibility_of_element_located((By.ID, "WebRTCVideo")))
assert preview_box.is_display(), "Preview doesn't appear to be running - terminate test and investigate."

def start_and_stop():
	start_live_ui(10)
	stop_recording_ui()
