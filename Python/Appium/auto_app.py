from appium import webdriver
import time
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

keyboard = KeyboardController()
mouse = MouseController()
#from pynput.keyboard import Key, Controller


"""At time of writing, very few of the above packages are being used because Appium and Selenium not playing nice"""



desired_caps = {}
desired_caps['platformName'] = 'Mac'
desired_caps['deviceName'] = 'MacBook'
desired_caps['app'] = 'Mediasite Mosaic'

mosaic = webdriver.Remote('http://0.0.0.0:4723/wd/hub', desired_caps, direct_connection = True)

#open_inputs = mosaic.find_element_by_id("_NS:55")

def change_record_mode(mode):
	open_inputs.click()
	
	rec_mode_box = mosaic.find_element_by_id("_NS:51")
	rec_mode_box.click()
	time.sleep(2)

	rec_mode_box.send_keys(mode)

	#keyboard.type(mode)
	#keyboard.press(Key.enter)
	#keyboard.release(Key.enter)


# Use this to bring the app back up while recording - mosaic.switch_to_window(1)

def get_stopRec_button_x_coord():
	stop_rec_butt = mosaic.find_element_by_id("_NS:42")
	stop_butt_coord = stop_rec_butt.location
	x = (list(stop_butt_coord.values())[list(stop_butt_coord.keys()).index("x")])
	return int(x)
	#y = (list(rec_butt_coord.values())[list(rec_butt_coord.keys()).index("y")])
	#actions.move_to

def get_stopRec_button_y_coord():
	stop_rec_butt = mosaic.find_element_by_id("_NS:42")
	stop_butt_coord = stop_rec_butt.location
	y = (list(stop_butt_coord.values())[list(stop_butt_coord.keys()).index("y")])
	return int(y)

# I am not proud of this hacky workaround
def start_a_recording():
	x_coord = get_stopRec_button_x_coord()
	y_coord = get_stopRec_button_y_coord()
	mouse.position = (x_coord, y_coord)
	mouse.move(-20, 20)
	time.sleep(1)
	mouse.click(Button.left, 1)

def set_title_and_start_recording(title):
	title_it = mosaic.find_element_by_id("_NS:12")
	title_it.click()
	time.sleep(2)
	keyboard.type(title)
	ok = mosaic.find_element_by_name("Ok")
	ok.click()
	cancel = mosaic.find_element_by_name("Cancel")
	cancel.click()

	start_a_recording()

	time.sleep(20)
	mosaic.switch_to_window(1)

	start_a_recording()
	time.sleep(10)
	start_a_recording()

	#not_like_this = mosaic.switch_to_active_element()
	#not_like_this.send_keys(title)

def start_recording():
	start_butt = mosaic.find_element_by_id("_NS:31")
	start_butt.click()

#Spam test
def rapid_fire_start_rec():
	time.sleep(5)
	start_a_recording()
	start_a_recording()
	start_a_recording()
	start_a_recording()


#set_title_and_start_recording(title="Automated Capture w/ Pauses")

def plz():
	recmod = mosaic.find_element_by_id("_NS:51")
	recmod.click()
	yah = mosaic.switch_to_active_element()
	yah.send_keys("Single Video")


#change_record_mode("Dual")

#x = get_startRec_button_x_coord()