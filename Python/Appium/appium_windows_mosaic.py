import pytest
from appium import webdriver
from api_mothership_titan import *
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import subprocess
import os
import capture_db_runner
import random
import getpass


#Using the DB python script to remove active mic and camera sources to perform a "fresh" test

desired_caps = {}
desired_caps["app"] = "SonicFoundryInc.MediasiteMosaic_nkm4rnn5kcqh2!App"

#Input Devices
life_cam = "Microsoft® LifeCam Studio(TM)"
life_cam_mic = "Desktop Microphone (Microsoft® LifeCam Studio(TM))"
realtek_mic = "Microphone (High Definition Audio Device)"
stereo_mic = "Stereo Mix (2- Realtek High Definition Audio)"
obsbot_cam = "OBSBOT Tiny Camera"
obsbot_mic = "Tiny Microphone (2- OBSBOT Tiny Audio)"


win_app_exe = ("C:\\Program Files (x86)\\Windows Application Driver\\WinAppDriver.exe")
mosaic_app_exe = ("C:\\Program Files\\WindowsApps\\SonicFoundryInc.MediasiteMosaic_2.2.23.0_x64__nkm4rnn5kcqh2\\SF.Mediasite.Capture.UWP.exe")



def getTasks(name):
    r = os.popen('tasklist /v').read().strip().split('\n')
    print ('# of tasks is %s' % (len(r)))
    for i in range(len(r)):
        s = r[i]
        if name in r[i]:
            #print ('%s in r[i]' %(name))
            return r[i]
    return []

def launch_winAppDriver():
    os.startfile(win_app_exe)

#Need to launch WinApplicationDriver.exe - check if it is running first
def check_winAppDr_running():
    if "Running" not in getTasks("Windows Application Driver"):
        print("Launching WinAppDriver...")
        launch_winAppDriver()

    elif "Running" in getTasks("Windows Application Driver"):
        print("WinAppDriver already running, launching Mosaic...")



check_winAppDr_running()
mosaic =  webdriver.Remote(command_executor="http://127.0.0.1:4723", desired_capabilities=desired_caps)

actions = ActionChains(mosaic)

def set_camera_and_mic_inputs(camera, mic):
	#This only works on first time start of Mosaic!

	# ex.) set_camera_and_mic_inputs(life_cam, realtek_mic)
	cam = mosaic.find_element_by_name(camera)
	cam.click()

	mic = mosaic.find_element_by_name(mic)
	mic.click()

buttons = mosaic.find_elements_by_class_name("AppBarButton")
mic_button = buttons[2]
camera_button = buttons[3]
screen_button = buttons[4]

def set_mic_input(mic):
	mic = mosaic.find_element_by_name(mic)
	mic.click()

def set_camera_input(camera):
	cam = mosaic.find_element_by_name(camera)
	cam.click()


def set_title(title):
	#We changed this recently (09/2020), code updated to reflect changes on 10/12/2020

	more_button = mosaic.find_element_by_name("More app bar")
	more_button.click()

	title_button = mosaic.find_element_by_name("Rename Presentation")
	time.sleep(1)
	title_button.click()

	title_field = mosaic.find_element_by_class_name("TextBox")
	title_field.clear()
	title_field.send_keys(title)
	time.sleep(1)

	ok_butt = mosaic.find_element_by_name("Ok")
	ok_butt.click()


def mic_check(mic):
	mic_button.click()
	mic_check = mosaic.find_element_by_name(mic)
	if mic_check.get_attribute("IsKeyboardFocusable") == "false":
		set_mic_input(mic)
		mic_button.click()
	else:
		mic_button.click()

def camera_check(camera):
	camera_button.click()
	camera_check = mosaic.find_element_by_name(camera)
	if camera_check.get_attribute("IsKeyboardFocusable") == "false":
		set_camera_input(camera)
		camera_button.click()
	else:
		camera_button.click()

def add_camera(camera):
	camera_button = mosaic.find_element_by_accessibility_id("VideoInputSelectorButton")
	camera_button.click()

	set_camera_input(camera)

def add_mic(mic):
	mic_button = mosaic.find_element_by_accessibility_id("AudioInputSelectorButton")
	mic_button.click()

	set_mic_input(mic)


def set_full_display(which_display):
	#screen_button.click()
	add_screen = mosaic.find_element_by_accessibility_id("ScreenCaptureInputSelectorButton")
	add_screen.click()

	time.sleep(1)
	
	dropdown = mosaic.find_element_by_name("Share your window")
	dropdown.click()

	share_display = mosaic.find_element_by_name("Share your display")
	share_display.click()

	set_display = mosaic.find_element_by_name(which_display)
	set_display.click()

	ok_it = mosaic.find_element_by_name("OK")
	ok_it.click()

def setup_dual_video_fullscreen(title, camera, mic, which_display):
	# ex.) setup_dual_video_fullscreen("Mosaic automated Dual Video", life_cam, realtek_mic, "Display 1")
	set_title(title=title)
	set_full_display(which_display)
	time.sleep(1)
	add_mic(mic)
	time.sleep(1)
	add_camera(camera)
	time.sleep(1)
	#mic_check(mic)
	#camera_check(camera)

def pause_it():
	mosaic.maximize_window()
	pause = mosaic.find_element_by_accessibility_id("RecordPauseButton")
	pause.click()

def resume_it():
	resume = mosaic.find_element_by_accessibility_id("RecordPauseButton")
	resume.click()

def stop_it():
	#The command below assumes the app is minimized.
	mosaic.launch_app()
	time.sleep(1)
	stop_rec = mosaic.find_element_by_accessibility_id("StopButton")
	stop_rec.click()

def one_min_pause():
	pause_it()
	time.sleep(60)
	resume_it()

# Hardcoding my input sources, check yours!
def dual_video_with_multiple_pauses(pause_count, duration):
	
	setup_dual_video_fullscreen("Mosaic automated Dual Video w/ Pauses", life_cam, realtek_mic, "Display 1")
	#Give the app a couple seconds to start previewing sources 
	time.sleep(2)
	resume_it()
	#Record for at least 10 sec before first Pause
	time.sleep(10)
	for _ in range(pause_count):
		one_min_pause()

	time.sleep(duration)
	stop_it()

def record_display_for(which_display, duration):
	set_full_display(which_display)
	time.sleep(2)
	resume_it()
	time.sleep(duration)
	stop_it()


def clear_preview_windows():
	#This is necessary because the "Close" element includes the X to quit the app

	#Nevermind this won't work - try again later
	app_box = mosaic.find_element_by_class_name("Windows.UI.Core.CoreWindow")

	previews = app_box.find_elements_by_accessibility_id("Close")
	for p in previews:
		p.click()

def start_recording(duration):
	rec = mosaic.find_element_by_accessibility_id("RecordPauseButton")
	rec.click()
	time.sleep(duration+2)

def switch_audio_source(source):
	mic_button = mosaic.find_element_by_accessibility_id("AudioInputSelectorButton")
	mic_button.click()

	mic = mosaic.find_element_by_name(source)
	mic.click()

def record_dual_video_and_switch_mics():
	setup_dual_video_fullscreen("Mosaic - 1 Min Dual Video " + str(random.randint(1, 100)), life_cam, realtek_mic, "Display 1")
	time.sleep(2)
	start_recording(60)
	stop_it()

def switch_to_presos_pg():
	preso_pg = mosaic.find_element_by_name("Presentations")
	if not preso_pg.is_selected():
		preso_pg.click()

def import_folder():
	switch_to_presos_pg()


	import_button = mosaic.find_element_by_name("Import")
	import_button.click()

	import_folder = mosaic.find_element_by_name("Import folder")
	import_folder.click()

	input("Pick a Folder, then press Enter to continue.")

def import_video():
	switch_to_presos_pg()

	import_button = mosaic.find_element_by_name("Import")
	import_button.click()

	import_video = mosaic.find_element_by_name("Import video")
	import_video.click()

	input("Pick an MP4 file, then press Enter to continue.")


def search_preso(preso_name):
	switch_to_presos_pg()

	search_button = mosaic.find_element_by_accessibility_id("ToggleSearchBarButton")
	search_button.click()

	search_field = mosaic.find_element_by_name("Searrch")
	search_field.send_keys(preso_name)

def filter_presos_by(filter_type):
	switch_to_presos_pg()

	filters = mosaic.find_element_by_accessibility_id("FilterButton")
	filters.click()

	filter_pick = mosaic.find_element_by_name(filter_type)
	filter_pick.click()

	#presos = mosaic.find_elements_by_class_name("ListViewItem")
	#play_top_result = presos[0].find_element_by_accessibility_id("OpenButton")
	#play_top_result.click()

	#context_top_result = presos[0].find_element_by_accessibility_id("MoreOptions")
	#open_local = mosaic.find_element_by_name("Open in Explorer")
def delayed_start_recording(which_display, delay_value, duration):
	# Ex.) delayed_start_recording("Display 1", 30, 60):
	set_full_display(which_display=which_display)
	#set_title(title="Mosaic display/window test runs, delayed start after " + str(delay_value) + " seconds.")
	
	# Hack to minimize Mosaic app window
	dummy = mosaic.find_element_by_accessibility_id("ScreenCaptureInputSelectorButton")
	dummy.send_keys(Keys.META + Keys.ARROW_DOWN)
	time.sleep(delay_value)
	
	mosaic.launch_app()
	time.sleep(3)
	#Immediately minimize app after clicking start record.  Maybe not if it keeps choking.
	start_recording(duration=duration)
	#constant_elements[0].send_keys(Keys.META + Keys.ARROW_DOWN)
	
	stop_it()

def delayed_start_recording_no_minimize(which_display, delay_value, duration):
	# Ex.) delayed_start_recording("Display 1", 30, 60):
	set_full_display(which_display=which_display)
	#set_title(title="Mosaic display/window test runs, delayed start after " + str(delay_value) + " seconds (no minimize).")
	
	time.sleep(delay_value)
	
	start_recording(duration=duration)
	#constant_elements[0].send_keys(Keys.META + Keys.ARROW_DOWN)
	
	stop_it()

def add_watch_folder():
	switch_to_presos_pg()

	import_button = mosaic.find_element_by_name("Import")
	import_button.click()

	import_video = mosaic.find_element_by_name("Add Watch Folder")
	import_video.click()

	input("Pick a Watch Folder, then press Enter to continue.")


def dual_video_run(duration):
	setup_dual_video_fullscreen(title="Mosaic for Windows - Automated Dual Video", camera=obsbot_cam, mic=realtek_mic, which_display="Display 1")
	time.sleep(1)
	start_recording(duration=duration)
	stop_it()

def check_menu_fly_not_exist():
	menu_fly = mosaic.find_element_by_class_name("MenuFlyout")
	assert not menu_fly.is_displayed, "Context clicking Scheduled Presentations should not reveal a flyout menu!"
	
def check_context_click_scheduled():
	switch_to_presos_pg()
	filter_presos_by("Scheduled")

	results = mosaic.find_elements_by_class_name("ListViewItem")
	actions.context_click(results[0])
	actions.perform()

	check_menu_fly_not_exist()