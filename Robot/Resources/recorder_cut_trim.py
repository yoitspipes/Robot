from rec_runner import *


def dual_video_slides_setup(preso_title, preso_setting):
	new_local_preso(preso_title=preso_title, preso_setting=preso_setting)
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

def preso_trim(preso_title):
	#nav_presos_pg()

	all_presos = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "presentation-item")))
	for p in all_presos:
		if preso_title in p.text:
			more = p.find_element(By.ID, "btnMore")
			more.click()

	trim = wait.until(EC.visibility_of_element_located((By.ID, "btnTrimPresentation")))
	trim.click()

	time.sleep(1)

	trim_start = wait.until(EC.visibility_of_element_located((By.NAME, "startTime")))
	trim_start.send_keys("00:00:03")

	trim_end = b.find_element(By.NAME, "endTime")
	trim_end.send_keys("00:00:15")

	save_copy = b.find_element(By.ID, "btnSaveAs")
	save_copy.click()

	#new_title = wait.until(EC.visibility_of_element_located((By.ID, "txtTitle")))
	#return new_title.get_property('value')

	time.sleep(1)

	apply_it = wait.until(EC.visibility_of_element_located((By.ID, "btnApply")))
	apply_it.click()

	#TODO - Find a better way to validate new preso is generated
	time.sleep(10)


	#refresh()

	#dumb_wait = wait.until(EC.visibility_of_element_located((By.ID, "btnSortBy")))

def preso_cut(preso_title):
	#nav_presos_pg()
	time.sleep(1)

	all_presos = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "presentation-item")))
	for p in all_presos:
		if preso_title in p.text:
			more = p.find_element(By.ID, "btnMore")
			more.click()

	cut = wait.until(EC.visibility_of_element_located((By.ID, "btnCutPresentation")))
	cut.click()

	time.sleep(1)

	cut_start = wait.until(EC.visibility_of_element_located((By.NAME, "startTime")))
	cut_start.send_keys("00:00:03")

	cut_end = b.find_element(By.NAME, "endTime")
	cut_end.send_keys("00:00:20")

	save_copy = b.find_element(By.ID, "btnSaveAs")
	save_copy.click()

	#new_title = wait.until(EC.visibility_of_element_located((By.ID, "txtTitle")))
	#return new_title.get_property('value')

	time.sleep(1)

	apply_it = wait.until(EC.visibility_of_element_located((By.ID, "btnApply")))
	apply_it.click()

	#TODO - Find a better way to validate new preso is generated
	time.sleep(10)

	#refresh()

	#dumb_wait = wait.until(EC.visibility_of_element_located((By.ID, "btnSortBy")))

def apply_trim_check_result(preso_title):
	new_title = preso_trim(preso_title=preso_title)

	apply_trim = b.find_element(By.ID, "btnApply")
	apply_trim.click()

	#TODO - Find a better way to validate new preso is generated
	time.sleep(10)

	all_presos = b.find_elements(By.CLASS_NAME, "presentation-item")
	for p in all_presos:
		if new_title in p.text:
			p.click()
	
	check_playback = wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "MediasitePlayerControls-CurrentTime"), "00:04"))
	assert check_playback, "Either playback failed or new presentation was not created"

	#Need to collapse playback preview for iterative test runs
	click_preso(preso_title=new_title)

def check_preso_playback(preso_title):
	#nav_presos_pg()
	time.sleep(1)

	all_the_presos = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "presentation-item")))
	for p in all_the_presos:
		if preso_title in p.text:
			p.click()

	check_playback = wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "MediasitePlayerControls-CurrentTime"), "00:04"))
	assert check_playback, "Either playback failed or new presentation was not created"



def apply_cut_check_result(preso_title):
	new_title = preso_cut(preso_title=preso_title)

	apply_cut = b.find_element(By.ID, "btnApply")
	apply_cut.click()

	#TODO - Find a better way to validate new preso is generated
	time.sleep(10)

	all_presos = b.find_elements(By.CLASS_NAME, "presentation-item")
	for p in all_presos:
		if new_title in p.text:
			p.click()