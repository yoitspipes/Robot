#This is meant to be used for Recorder Express
from chrome_launcher import *
import rec_creds

short_wait = WebDriverWait(b, 5)
b.maximize_window()

def login_recorder():
	user = b.find_element(By.ID, "txtLogin")
	user.send_keys(rec_creds.USERNAME)
	pwd = b.find_element(By.ID, "txtPassword")
	pwd.send_keys(rec_creds.PASSWORD)

	login = b.find_element(By.ID, "btnLogin")
	login.click()


def launch_recorder_web():
	b.maximize_window
	rec_link = ("http://" + rec_creds.IP_ADDRESS + ":8090/RecorderUI")
	b.get(rec_link)

	#There may be occassions where login form does not appear
	try:
		login_modal = short_wait.until(EC.visibility_of_element_located((By.NAME, "loginForm")))

		if login_modal.is_displayed():
			login_recorder()
			time.sleep(1)
		else:
			print("Login modal not visible, proceeding...")

	except TimeoutException:
		print("No login modal appeared within timeout, proceeding...")

def open_settings():

	settings = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Settings")))
	settings.click()

def open_inputs():

	input_sel = wait.until(EC.visibility_of_element_located((By.ID, "btnInputSelect")))
	input_sel.click()

	inputs = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "InputSectionTitle")))

	#Expect to see local inputs opened by default but sometimes it doesn't exist
	close_all_chevrons()

def close_inputs():
	input_sel = wait.until(EC.visibility_of_element_located((By.ID, "btnInputSelect")))
	input_sel.click()

def check_login_then_open_settings():
	#Sometimes the login form appears, most often it doesn't but need some logic to deal with that...
	try:
		short_wait.until(EC.visibility_of_element_located((By.NAME, "loginForm")))
		login_recorder()
		open_settings()

	except:
		open_settings()


def nav_presos_pg():
	presos_tab = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-presentations")))
	presos_tab.click()

def nav_sched_pg():
	sched_tab = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-schedules")))
	sched_tab.click()

def rename_preso(new_title):
	title_box = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "icon-pencil")))
	title_box.click()

	title_field = wait.until(EC.visibility_of_element_located((By.ID, "txtTitle")))
	title_field.clear()
	title_field.send_keys(new_title)

	time.sleep(1)

	ok = b.find_element(By.ID, "btnOk")
	ok.click()

def get_recorder_state():
	current_state = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "recorder-status")))
	return current_state.text

def check_recorder_state(expected_state):
	state_check = wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "recorder-status"), expected_state))

def check_preso_title(preso_title):
	preso_title_field = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "recorder-title")))
	assert preso_title in preso_title_field.text, "Unexpected presentation title detected, title is: '" + preso_title_field.text + "'"

def new_local_preso(preso_title, preso_setting):
	new_butt = wait.until(EC.visibility_of_element_located((By.ID, "btnNew")))
	new_butt.click()

	title_box = wait.until(EC.visibility_of_element_located((By.ID, "txtTitle")))
	title_box.clear()
	title_box.send_keys(preso_title)

	preso_settings = b.find_elements(By.CLASS_NAME, "settings-list-item")
	
	for p in preso_settings:
		if preso_setting in p.text:
			p.click()

	create_it = b.find_element(By.ID, "btnAdd")
	create_it.click()




def open_mvp_conns():
	mvp_conn = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Mediasite Connections")))
	mvp_conn.click()

	time.sleep(2)

	dumb_wait = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "mediasite-server-connections-wrapper")))

	assert dumb_wait.is_displayed(), "Something broke getting to the Mediasite Connections page"

def down_chevs_count():
	chevs = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "icon-chevron-down-white")))
	return chevs

def close_chevron():
	chevs = b.find_elements(By.CLASS_NAME, "icon-chevron-down-white")
	chevs[0].click()

def close_all_chevrons():
	down_chevs = down_chevs_count()

	for i in range(len(down_chevs)):
		close_chevron()

def change_mvp_conn(mvp_site):

	time.sleep(1)
	conns = b.find_elements(By.CLASS_NAME, "mediasite-server-connection-item-root-url")
	time.sleep(1)
	
	for conn in conns:
		if mvp_site in conn.text:
			conn.click()
			time.sleep(2)
			break

def sched_checkbox():
	checkboxes = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "settings-form-row")))
	
	for check in checkboxes:
		if "Enable Scheduler" in check.text:
			enable_sched = check.find_element(By.CLASS_NAME, ("iCheck-helper"))
			enable_sched.click()
			break

def set_sched_titan():
	conns = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "scheduler-connection-item")))
	for conn in conns:
		if "titan" in conn.text:
			conn.click()

def toggle_scheduler():
	settings_page = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Settings")))
	settings_page.click()

	sched_conn = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Scheduler Connections")))
	sched_conn.click()

	sched_checkbox()
	time.sleep(4)
	sched_checkbox()
	time.sleep(2)
	#set_sched_titan() - this needs some work when it is already set to titan

def add_chapter():
	chapter = wait.until(EC.visibility_of_element_located((By.ID, "btnInsertChapter")))
	chapter.click()

def open_file_sources():
	inputs = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "input-list")))

	for i in inputs:
		if "File" in i.text:
			i.find_element(By.CLASS_NAME, "listIcon").click()

	time.sleep(1)

def open_preso(preso_title):
	open_button = wait.until(EC.visibility_of_element_located((By.ID, "btnOpen")))
	open_button.click()

	search_box = wait.until(EC.visibility_of_element_located((By.ID, "txtSearch")))
	search_box.send_keys(preso_title)

	results = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "grid-row-title")))

	for r in results:
		if preso_title in r.text:
			r.click()
			do_it = wait.until(EC.visibility_of_element_located((By.ID, "btnPublish")))
			do_it.click()


def change_slide_input_file_source(input_name):
	#close_all_chevrons()
	#open_file_sources()

	sources = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "inputSourceFileItem")))

	for s in sources:
		if input_name in s.text:
			s.click()

	map_to_slide = wait.until(EC.visibility_of_element_located((By.ID, "btnRouteSlide")))
	map_to_slide.click()

	time.sleep(1)

	#close_all_chevrons()
	#time.sleep(1)

def change_slide_input_test_source(input_name):
	#close_all_chevrons()
	#open_file_sources()
	time.sleep(1)

	sources = b.find_elements(By.CLASS_NAME, "inputSourceItem")

	for s in sources:
		if input_name in s.text:
			s.click()

	map_to_slide = wait.until(EC.visibility_of_element_located((By.ID, "btnRouteSlide")))
	map_to_slide.click()

	time.sleep(1)

	#close_all_chevrons()
	#time.sleep(1)

def open_local_sources():
	inputs = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "input-list")))

	for i in inputs:
		if "Local" in i.text:
			i.find_element(By.CLASS_NAME, "listIcon").click()

	time.sleep(1)

def expand_input(input_type):
	types = b.find_elements(By.CLASS_NAME, "inputTitleExpander")
	for t in types:
		if input_type in t.text:
			t.click()

def collapse_input(input_type):
	types = b.find_elements(By.CLASS_NAME, "inputTitleExpander")
	for t in types:
		if input_type in t.text:
			t.click()

def open_usb_sources():
	inputs = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "input-list")))

	for i in inputs:
		if "USB" in i.text:
			i.find_element(By.CLASS_NAME, "listIcon").click()

	time.sleep(1)

def change_vid1_input(input_name):
	time.sleep(1)
	sources = b.find_elements(By.CLASS_NAME, "inputSourceDescription")

	for s in sources:
		if input_name in s.text:
			s.click()

	map_to_vid1 = wait.until(EC.visibility_of_element_located((By.ID, "btnRouteVideo1")))
	map_to_vid1.click()

def change_slide_input(input_name):
	sources = b.find_elements(By.CLASS_NAME, "inputSelectorContent")

	for s in sources:
		if input_name in s.text:
			s.click()

	map_to_slide = wait.until(EC.visibility_of_element_located((By.ID, "btnRouteSlide")))
	map_to_slide.click()

#Assumes input source modal is already opened!
def set_audio():
	map_to_audio = wait.until(EC.visibility_of_element_located((By.ID, "btnRouteAudio")))
	map_to_audio.click()


def audio_input(input_name):
	time.sleep(1)
	sources = b.find_elements(By.CLASS_NAME, "inputSourceItem")

	for s in sources:
		if input_name in s.text:
			s.click()

	map_to_audio = wait.until(EC.visibility_of_element_located((By.ID, "btnRouteAudio")))
	map_to_audio.click()

def open_test_sources():
	inputs = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "input-list")))

	for i in inputs:
		if "Test" in i.text:
			i.find_element(By.CLASS_NAME, "listIcon").click()

	time.sleep(1)

def start_recording_ui(start_duration):
	rec = wait.until(EC.visibility_of_element_located((By.ID, "btnRecord")))
	rec.click()

	time.sleep(start_duration)

def start_live_ui(start_duration):
	rec = wait.until(EC.visibility_of_element_located((By.ID, "btnGoLive")))
	rec.click()

	new_status = wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "footer-status-text"), "Recording"))
	assert new_status, "Status should be 'Recording' but is: " + new_status

def pause_recording_ui(pause_duration):
	pause = wait.until(EC.visibility_of_element_located((By.ID, "btnPause")))
	pause.click()

	time.sleep(pause_duration)

def resume_recording_ui(resume_duration):
	resume = wait.until(EC.visibility_of_element_located((By.ID, "btnResume")))
	resume.click()

	time.sleep(resume_duration)

def stop_recording_ui():
	stop = wait.until(EC.visibility_of_element_located((By.ID, "btnStop")))
	stop.click()

	new_status = wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "footer-status-text"), "Idle"))
	assert new_status, "Status should be 'Idle' but is: " + new_status

def delete_preso(preso_title):
	nav_presos_pg()

	all_presos = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "presentation-item")))
	for p in all_presos:
		if preso_title in p.text:
			delete = p.find_element(By.ID, "btnDelete")
			delete.click()

	delete_confirm = wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "confirm-content"), "Are you sure you want to permanently delete this presentation?"))
	assert delete_confirm, "There should be a confirmation of deletion here"

	do_it = b.find_element(By.ID, "btnOk")
	do_it.click()

	time.sleep(2)

def refresh():
	b.refresh()

def terminate():
	b.quit()

def recon_recorders(rec_name):
	launch_recorder_web(rec_name=rec_name)
	open_settings()
	time.sleep(1)
	open_mvp_conns()
	change_mvp_conn("demo")
	time.sleep(1)
	change_mvp_conn("titan")
	time.sleep(1)
	toggle_scheduler()
	time.sleep(1)

def slide_changer():
	open_inputs()
	open_file_sources()
	change_slide_input_file_source("Technical")
	time.sleep(2)
	change_slide_input_file_source("Screenshot")
	time.sleep(2)
	change_slide_input_file_source("Intermission")
	time.sleep(2)
	open_test_sources()
	time.sleep(2)
	change_slide_input_test_source("Gray Bars")
	time.sleep(2)
	#change_slide_input("spidey")
	#time.sleep(2)
	close_inputs()

def vid1_changer():
	open_inputs()
	#open_test_sources()
	open_local_sources()
	time.sleep(1)
	#expand_input("Local Sources")
	change_vid1_input("SDI")
	audio_input("SDI")
	time.sleep(2)
	#collapse_input("Local Sources")
	time.sleep(1)
	expand_input("USB Sources")
	time.sleep(1)
	change_vid1_input("Microsoft LifeCam")
	#audio_input("LifeCam") - needs work
	time.sleep(2)
	change_vid1_input("RealSense")
	time.sleep(2)
	collapse_input("USB Sources")
	time.sleep(1)
	change_vid1_input("(HDMI, DVI-D)")
	audio_input("RCA")
	time.sleep(1)
	close_inputs()


def rl15_mp4_slide_test():
	#open_preso("PRESO TITLE HERE")
	#start_recording_ui()
	#time.sleep(10)
	open_inputs()
	time.sleep(1)
	expand_input("File Sources")
	time.sleep(1)
	change_slide_input("Technical")
	time.sleep(1)
	add_chapter()
	time.sleep(30)
	change_slide_input("rdr2")
	time.sleep(1)
	add_chapter()
	time.sleep(60)
	collapse_input("File Sources")
	time.sleep(1)
	expand_input("Test Sources")
	change_slide_input("Gray Bars")
	time.sleep(1)
	add_chapter()
	time.sleep(30)
	collapse_input("Test Sources")
	time.sleep(1)
	expand_input("USB Sources")
	time.sleep(1)
	change_slide_input("RealSense")
	time.sleep(1)
	add_chapter()
	time.sleep(30)
	collapse_input("USB Sources")
	time.sleep(1)
	expand_input("File Sources")
	#change_vid1_input("rdr2")
	#set_audio()
	time.sleep(1)
	change_slide_input("Intermission")
	time.sleep(1)
	add_chapter()
	time.sleep(30)
	collapse_input("File Sources")
	time.sleep(1)
	expand_input("USB Sources")
	change_vid1_input("RealSense")
	time.sleep(1)
	add_chapter()
	time.sleep(1)
	collapse_input("USB Sources")
	time.sleep(1)
	expand_input("Test Sources")
	change_slide_input("Gray Bars")
	time.sleep(1)
	add_chapter()
	collapse_input("Test Sources")
	time.sleep(60)
	#pause_recording_ui(60)
	#resume_recording_ui(5)
	expand_input("USB Sources")
	time.sleep(1)
	change_vid1_input("LifeCam")
	add_chapter()
	time.sleep(1)
	change_slide_input("RealSense")
	time.sleep(1)
	collapse_input("USB Sources")
	time.sleep(30)
	expand_input("Test Sources")
	time.sleep(1)
	change_slide_input("Gray Bars")
	add_chapter()
	time.sleep(60)
	stop_recording_ui()


#rec_names = ["QA-RL220", "QA-R1020A", "QA-RL940R0", "005-6830659"]
#[recon_recorders(rec_name) for rec_name in rec_names]