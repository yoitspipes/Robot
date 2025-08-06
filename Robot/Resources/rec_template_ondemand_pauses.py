#IN PROGRESS
from rec_runner import *

def dual_video_setup(preso_title):
	rename_preso(new_title=preso_title)
	title_wait = wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "recorder-title"), preso_title))
	assert title_wait, "Presentation's title is not correct"
	time.sleep(1)

	state_check = wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "recorder-status"), "Idle"))
	assert state_check, "Recorder took too long to transition to 'Idle' state after opening new Presentation"

def record_preso(duration):
	start_recording_ui(start_duration=duration)
	stop_recording_ui()

	#Default title should update to 'Untitled-xxx'
	title_wait = wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "recorder-title"), "Untitled"))
	assert title_wait, "Unexepected title detected, check if Recorder app has hung"

