import base64
import requests
import re
import datetime
import time
import os
import pdb
import json
from random import randint
import rec_creds

requests.packages.urllib3.disable_warnings()

"""This is the API mothership.  Many Mediasite endpoints - mostly around scheduling."""

#Feel free to add to this
annotations_api = (rec_creds.MVP_URL + "/Api/v1/" + "Annotations")
catalog_api = (rec_creds.MVP_URL + "/Api/v1/" + "Catalogs")
catch_devices = (rec_creds.MVP_URL + "/Api/v1/" + "CatchDevices")
categories_api = (rec_creds.MVP_URL + "/Api/v1/" + "Categories")
folder_api = (rec_creds.MVP_URL + "/Api/v1/" + "Folders")
channels_api = (rec_creds.MVP_URL + "/Api/v1/" + "MediasiteChannels")
import_projects_api = (rec_creds.MVP_URL + "/Api/v1/" + "MediaImportProjects")
modules_api = (rec_creds.MVP_URL + "/Api/v1/" + "Modules")
players_api = (rec_creds.MVP_URL + "/Api/v1/" + "Players")
playlists_api = (rec_creds.MVP_URL + "/Api/v1/" + "Playlists")
preso_api = (rec_creds.MVP_URL + "/Api/v1/" + "Presentations")
presenters_api = (rec_creds.MVP_URL + "/Api/v1/" + "Presenters")
recorders_api = (rec_creds.MVP_URL + "/Api/v1/" + "Recorders")
room_configs_api = (rec_creds.MVP_URL + "/Api/v1/" + "RoomConfigurations")
rooms_api = (rec_creds.MVP_URL + "/Api/v1/" + "Rooms")
schedule_api = (rec_creds.MVP_URL + "/Api/v1/" + "Schedules")
mosaic_schedule_api = (rec_creds.MVP_URL + "/Api/v1/" + "MosaicSchedules")
showcases_api = (rec_creds.MVP_URL + "/Api/v1/" + "Showcases")
templates_api = (rec_creds.MVP_URL + "/Api/v1/" + "Templates")
user_profiles_api = (rec_creds.MVP_URL + "/Api/v1/" + "UserProfiles")
vodcasts_api = (rec_creds.MVP_URL + "/Api/v1/" + "VideoPodcastProjects")
presentationquizzes_api = (rec_creds.MVP_URL + "/Api/v1/" + "PresentationQuizzes")
home = (rec_creds.MVP_URL + "/Api/v1/" + "Home")





#We'll set the recurrence either in minutes or hours from current time (m1 = 1 min, h1= 1 hr, etc.).
#now = datetime.datetime.now()
#Need to convert to iso format for API compliance

#utc1 = ((datetime.datetime.now(timezone.utc).replace(microsecond=0)) + datetime.timedelta(hours=0, minutes=1)).isoformat()
m1 = ((datetime.datetime.now().replace(microsecond=0)) + datetime.timedelta(hours=5, minutes=1)).isoformat()
m2 = ((datetime.datetime.now().replace(microsecond=0)) + datetime.timedelta(hours=5, minutes=2)).isoformat()
m3 = ((datetime.datetime.now().replace(microsecond=0)) + datetime.timedelta(hours=5, minutes=3)).isoformat()
m4 = ((datetime.datetime.now().replace(microsecond=0)) + datetime.timedelta(hours=5, minutes=4)).isoformat()
m5 = ((datetime.datetime.now().replace(microsecond=0)) + datetime.timedelta(hours=5, minutes=5)).isoformat()
m10 = ((datetime.datetime.now().replace(microsecond=0)) + datetime.timedelta(hours=5, minutes=10)).isoformat()
m15 = ((datetime.datetime.now().replace(microsecond=0)) + datetime.timedelta(hours=5, minutes=15)).isoformat()
m20 = ((datetime.datetime.now().replace(microsecond=0)) + datetime.timedelta(hours=5, minutes=20)).isoformat()
m30 = ((datetime.datetime.now().replace(microsecond=0)) + datetime.timedelta(hours=5, minutes=30)).isoformat()
m40 = ((datetime.datetime.now().replace(microsecond=0)) + datetime.timedelta(hours=5, minutes=40)).isoformat()
m45 = ((datetime.datetime.now().replace(microsecond=0)) + datetime.timedelta(hours=5, minutes=45)).isoformat()
h1 = ((datetime.datetime.now().replace(microsecond=0)) + datetime.timedelta(hours=6, minutes=0)).isoformat()
h2 = ((datetime.datetime.now().replace(microsecond=0)) + datetime.timedelta(hours=7, minutes=0)).isoformat()
h3 = ((datetime.datetime.now().replace(microsecond=0)) + datetime.timedelta(hours=8, minutes=0)).isoformat()
h4 = ((datetime.datetime.now().replace(microsecond=0)) + datetime.timedelta(hours=9, minutes=0)).isoformat()
h5 = ((datetime.datetime.now().replace(microsecond=0)) + datetime.timedelta(hours=10, minutes=0)).isoformat()
h6 = ((datetime.datetime.now().replace(microsecond=0)) + datetime.timedelta(hours=11, minutes=0)).isoformat()


headers = {
"sfapikey": rec_creds.API_KEY, 
"Content-Type": "application/json",
"Authorization": "Basic " + base64.b64encode((rec_creds.MVP_USER + ":" + rec_creds.MVP_PASS).encode("ascii")).decode("ascii")
}


def get_site_version():
	url = home
	home_info = requests.get(url, headers = headers, verify = False)
	assert home_info.status_code == 200, "Could not hit the API endpoint for Home?!  Check on it!"
	jsonData = home_info.json()

	site_version = jsonData.get("SiteVersion")
	site_build = jsonData.get("SiteBuildNumber")
	return site_version, site_build



todays_date = datetime.datetime.utcnow().date().isoformat()

#We'll get the folder id of your preferred folder if specified in the creds file.

def get_user_profile_id(user):
	url = (user_profiles_api + "?$top=1000")
	get_user_profiles = requests.get(url, headers = headers, verify = False)
	assert get_user_profiles.status_code == 200, "Can't hit the UserProfiles endpoint, check on it!"
	jsonData = get_user_profiles.json()

	for result in get_user_profiles.json()['value']:
		if result['DisplayName'] in user:
			that_user_profile_id = result['Id']
			return that_user_profile_id

def get_catch_user_ids():
	url = (user_profiles_api + "?$top=1000")
	get_user_profiles = requests.get(url, headers = headers, verify = False)
	assert get_user_profiles.status_code == 200, "Can't hit the UserProfiles endpoint, check on it!"
	jsonData = get_user_profiles.json()

	for result in get_user_profiles.json()['value']:
		if result['HasHomeFolder'] == False:
			catch_user_ids = result['Id']
			return catch_user_ids


def delete_user_profile(user):
	user_id = get_user_profile_id(user)
	url = (user_profiles_api + "('" + user_id + "')")
	delete_profile = requests.delete(url, header = headers, verify = False)
	return delete_profile.status_code



def get_a_catch_id(name):
	url = (catch_devices + "?$top=100")
	get_catch_devices = requests.get(url, headers = headers, verify = False)
	assert get_catch_devices.status_code==200, "Can't hit the CatchDevices endpoint, check on that!"
	jsonData = get_catch_devices.json()

	for result in get_catch_devices.json()['value']:
		if result['Name'] == name:
			that_cat_id = result['Id']
			return that_cat_id


def get_my_folder_id():
	url = (folder_api + "?$top=500")
	get_folders = requests.get(url, headers = headers, verify = False)
	assert get_folders.status_code == 200, "That folder does not exist! Or you don't have access to it..."
	jsonData = get_folders.json()

	for result in get_folders.json()['value']:
		if result["Name"] == config.default_folder:
			my_folder_id = result["Id"]
			return my_folder_id


#my_folder_id = get_my_folder_id()

def get_a_recorder_id(rec_name):
	url = (recorders_api + "?$top=100")
	get_recs = requests.get(url, headers=headers, verify=False)
	assert get_recs.status_code == 200, "Can't retrieve the Recorders!"
	jsonData = get_recs.json()

	for result in get_recs.json()['value']:
		if result["Name"] == rec_name:
			my_rec_id = result["Id"]
			return my_rec_id


def get_my_cat_id(cat_name):
	url = (catch_devices + "?$top=100")
	get_cats = requests.get(url, headers = headers, verify = False)
	assert get_cats.status_code == 200, "Can't find the Catch devices"
	jsonData = get_cats.json()

	for result in get_cats.json()['value']:
		if result["Name"] == cat_name:
			my_cat_id = result["Id"]
			return my_cat_id

def get_my_folder_id():
	url = (folder_api + "?$top=500")
	get_folders = requests.get(url, headers = headers, verify = False)
	assert get_folders.status_code == 200, "That folder does not exist! Or you don't have access to it..."
	jsonData = get_folders.json()

	for result in get_folders.json()['value']:
		if result["Name"] == config.default_folder:
			my_folder_id = result["Id"]
			return my_folder_id


def get_todays_presos():
	url = (preso_api + "?$top=1000000")
	get_all_presos = requests.get(url, headers = headers, verify = False)
	assert get_all_presos.status_code == 200, "Can't hit the Presentations endpoint, wtf is happening?!"
	jsonData = get_all_presos.json()

	for result in get_all_presos.json()['value']:
		if todays_date in result["RecordDate"]:
			return result["Id"]

def get_a_user_profile(name):
	url = (user_profiles_api + "?$top=1000")
	get_profs = requests.get(url, headers = headers, verify = False)
	assert get_profs.status_code == 200, "Can't hit UserProfiles endpoint, full error: " + get_profs.response
	jsonData = get_profs.json()

	for result in get_profs.json()['value']:
		if result["UserName"] == name:
			user_folder_id = result["HomeFolderId"]
			return user_folder_id


def get_a_showcase_id(name):
	url = (showcases_api + "?$top=100")
	get_shows = requests.get(url, headers=headers, verify=False)
	assert get_shows.status_code == 200, "That Showcase doesn't exist!  Or access issues, or endpoint broken.."
	jsonData = get_shows.json()

	for result in get_shows.json()['value']:
		if result["Name"] == name:
			that_show_id = result["Id"]
			return that_show_id

def get_a_folder_id(name):
	url = (folder_api + "?$top=1000")

	get_folders = requests.get(url, headers = headers, verify = False)
	assert get_folders.status_code == 200, ("That folder does not exist! Or you don't have access to it..." + str(get_folders.status_code))
	jsonData = get_folders.json()

	for result in get_folders.json()['value']:
		if result["Name"] == name:
			that_folder_id = result["Id"]
			return that_folder_id

def get_a_template_id(name):
	url = (templates_api  + "?$top=1000")

	get_templates = requests.get(url, headers=headers, verify=False)
	assert get_templates.status_code == 200, "Can't hit the Templates API endpoint, check on that!"
	jsonData = get_templates.json()

	for result in get_templates.json()['value']:
		if result["Name"] == name:
			that_template_id = result["Id"]
			return that_template_id

def get_a_catalog_id(name):
	url = (catalog_api + "?$top=100")

	get_catalogs = requests.get(url, headers=headers, verify=False)
	assert get_catalogs.status_code==200, "Can't hit the Catalogs API endpoint, check on that!"
	jsonData = get_catalogs.json()

	for result in get_catalogs.json()['value']:
		if result["Name"] == name:
			that_catalog_id = result["Id"]
			return that_catalog_id

def get_a_preso_id(title):
	url = (preso_api+"?$top=1000")

	get_presos = requests.get(url, headers=headers, verify=False)
	assert get_presos.status_code == 200, "That presentation doesn't exists!  Or access issues, things borked, etc."
	
	for result in get_presos.json()['value']:
		if result["Title"] == title:
			that_preso_id = result["Id"]
			return that_preso_id

def get_a_player_id(name):
	url = (players_api+"?$top=100")

	get_players = requests.get(url, headers=headers, verify=False)
	assert get_players.status_code==200, "Could not hit the PLayers API endpoint, check on it!"

	for result in get_players.json()['value']:
		if result['Name']== name:
			that_player_id = result["Id"]
			return that_player_id

def get_a_schedule_id(name):
	url = (schedule_api + "?$top=1000")
	get_schedules = requests.get(url, headers=headers, verify=False)
	assert get_schedules.status_code==200, "Could not hit the Schedules API endpoint, what's up with that??"

	for result in get_schedules.json()['value']:
		if result['Name']==name:
			that_schedule_id = result['Id']
			return that_schedule_id

def get_a_module_id(mod_name):
	url = (modules_api + "?$top=1000")

	get_modules = requests.get(url, headers=headers, verify=False)
	assert get_modules.status_code == 200, "That Module doesn't exists!  Or access issues, things borked, etc."
	
	for result in get_modules.json()['value']:
		if result["Name"] == mod_name:
			that_mod_id = result["Id"]
			return that_mod_id

def api_quiz1(title):
	presentation_id = get_a_preso_id(title)
	url = presentationquizzes_api

	payload = {
		"Name": "Bill Gates bitchn quiz1",
		"Description": "",
		"Creator": rec_creds.MVP_USER,
		"Type": "StudyGuide",
		"ShowScore": True,
		"ShowAnswers": True,
		"PresentationId": presentation_id,
		"PublishedState": "Published"
		}
	quiz_post = requests.post(url, headers = headers, data = json.dumps(payload), verify = False)
	quiz_post.raise_for_status()

	jsonData = quiz_post.json()
	my_quiz_id = jsonData["Id"]
	return my_quiz_id

def delete_schedule(schedule_name):
	sched_id = get_a_schedule_id(schedule_name)

	url = (schedule_api + "('" + sched_id + "')")

	delete_schedule = requests.delete(url, headers=headers, verify=False)
	delete_schedule.raise_for_status()

def delete_showcase(show_name):
	show_id = get_a_showcase_id(show_name)

	url = (showcases_api + "('" + show_id + "')")

	delete_showcase = requests.delete(url, headers=headers, verify=False)
	delete_showcase.raise_for_status()


def set_showcase_theme(show_name, theme):
	show_id = get_a_showcase_id(show_name)
	
	url = (showcases_api + "/('" + show_id + "')")

	payload = {
		"Theme": theme
		}

	show_patch = requests.patch(url, headers = headers, data = json.dumps(payload), verify = False)
	show_patch.raise_for_status()


def create_mediasite_channel(channel_name):
	payload = {
		"Name": channel_name,
		"IsMyMediasiteChannel": False,
		"IsSearchBased": False,
		"IsPublishingTabCatalog": True,
		"ShowInPublishingTab": True,
		#"RegistrationRequired": False, - this apparently causes the POST to fail, despite it being included in the API docs
		"IsChannel": True
	}
	url = channels_api

	channel_post = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
	channel_post.raise_for_status()

def create_mediasite_channel_search(channel_name, search_term):
	payload = {
		"Name": channel_name,
		"IsMyMediasiteChannel": False,
		"IsSearchBased": True,
		"SearchTerm": search_term,
		#"SearchFields": "Tags",
		"IsPublishingTabCatalog": True,
		"ShowInPublishingTab": True,
		#"RegistrationRequired": False, - this apparently causes the POST to fail, despite it being included in the API docs
		"IsChannel": True
	}
	url = channels_api

	channel_post = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
	channel_post.raise_for_status()

#Function below is one variation of the many Channel properties than be configured - feel free to clone it and apply your own configuration to the clone
def showcase_spotlight_post(show_name, preso_name):
	show_id = get_a_showcase_id(name=show_name)
	preso_id = get_a_preso_id(title=preso_name)

	url = (showcases_api+"('"+show_id+"')"+"/PublishToSpotlight")
	
	payload = {
		"PresentationIds": [preso_id]
		}

	spot_post = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
	spot_post.raise_for_status()

def get_root_folder_id():
	url = (rec_creds.MVP_URL + "/Api/v1/" + "Home")
	req = requests.get(url, headers = headers, verify = False)
	assert req.status_code == 200
	jsonData = req.json()
	root_folder = jsonData["RootFolderId"]
	return root_folder


#root_folder = get_root_folder_id()

def api_external_catch_project(import_name, folder_name, template_name, path):
	#ex.) api_external_catch_project("Pipes' External Media Imports", "External Imports", "HD Single MP4", "\\\\angstrom.sofoqa.net\data\pipes\AVEngine\Samples")
	#template_name
	import_folder_id = get_a_folder_id(folder_name)

	template_id = get_a_template_id(template_name)

	url = import_projects_api

	payload = {
		"Name": import_name,
		"UpdateInterval": 60,
		"PresentationTemplateId": template_id,#config.desktop_camera_template_id, #template_name
		"DropBoxDetails": {
			"Location": path, 
			"Username": rec_creds.MVP_USER,
			"Password": rec_creds.MVP_PASS
			},
		"ImportOptions": {
			"AlwaysUsePresentersFromTemplate": True,
			"DeleteDropboxFileOnSuccessfulImport": False,
			"StartTimeUtc": m1,
			"ImportFolderId": import_folder_id,
			"TitlePresentationBasedOnTemplate": False,
			"MaxMediaQualityDeterminedByTemplate": False
			},
		#ProjectType can also be 'Default', 'MediasitePackageImport'
		#"ParentFolderId": "cb343b92836e4d648a3e645ba97a062014",
		"ProjectType": "ExternalMediaImport"

		}

	proj_post = requests.post(url, headers = headers, data = json.dumps(payload), verify = False)
	post_result = proj_post.raise_for_status()
	return post_result

def api_external_import_project(import_name, folder_name, template_name, path):
	#ex.) api_external_import_project("Pipes' Untamed External Imports", "External Imports", "HD Single MP4", "\\\\angstrom.sofoqa.net\\data\\pipes\\ximports")
	
	import_folder_id = get_a_folder_id(folder_name)

	template_id = get_a_template_id(template_name)

	url = import_projects_api

	payload = {
		"Name": import_name,
		"UpdateInterval": 60,
		"PresentationTemplateId": template_id,#config.desktop_camera_template_id, #template_name
		"DropBoxDetails": {
			"Location": path, 
			"Username": rec_creds.MVP_USER,
			"Password": rec_creds.MVP_PASS
			},
		"ImportOptions": {
			"AlwaysUsePresentersFromTemplate": False,
			"DeleteDropboxFileOnSuccessfulImport": False,
			"StartTimeUtc": m10,
			"ImportFolderId": import_folder_id,
			"TitlePresentationBasedOnTemplate": False
			#"MaxMediaQualityDeterminedByTemplate": template_enforced
			},
		#ProjectType can also be 'Default', 'MediasitePackageImport'
		#"ParentFolderId": "cb343b92836e4d648a3e645ba97a062014",
		"ProjectType": "ExternalMediaImport"

		}

	proj_post = requests.post(url, headers = headers, data = json.dumps(payload), verify = False)
	post_result = proj_post.raise_for_status()
	return post_result
	

def create_presenter(first):
	url = presenters_api

	payload = {
		"FirstName": first,
		#"MiddleName": "keke",
		"Email": "presenter_without_last@name"
	}

	presenter_post = requests.post(url, headers=headers, data = json.dumps(payload), verify = False)
	post_result = presenter_post.raise_for_status()
	return post_result

def annotate_a_preso(preso_name, annotation_title, annotation, position):
	preso_id = get_a_preso_id(title=preso_name)

	url = (preso_api + "('" + preso_id + "')" + "/Annotations")

	payload = {
		"Position": int(position),
		"Title": annotation_title,
		"AnnotationText": annotation,
		"IsVisible": True
		
	}

	annotation_post = requests.post(url, headers = headers, data = json.dumps(payload), verify = False)
	post_result = annotation_post.raise_for_status()
	return post_result




def comment_a_preso(preso_name, comment):
	preso_id = get_a_preso_id(title=preso_name)

	url = (preso_api + "('" + preso_id + "')" + "/Comments")

	payload = {
		"UserName": rec_creds.MVP_USER,
		"DisplayName": rec_creds.MVP_USER,
		"Text": comment,
		"UiPresentationId": preso_id,
		"IsVisible": True
	}

	comment_post = requests.post(url, headers=headers, data = json.dumps(payload), verify = False)
	post_result= comment_post.raise_for_status()
	return post_result




def api_live_video_schedule(time_from_now, duration, rec_name, folder_name, template_name):
	rec_id = get_a_recorder_id(rec_name)
	template_id = get_a_template_id(template_name)
	folder_id = get_a_folder_id(folder_name)

	payload = {"Name": rec_name + " Single Video Live Stream " + str(randint(0,50)),
		"Description": "Testing live single video only on  " + rec_name, 
		"DeviceId": rec_id, 
		"ScheduleTemplateId": template_id, #template_name
		"TitleType": "ScheduleNameAndNumber", 
		"FolderId": folder_id, 
		"CreatePresentation": True, 
		"AdvanceCreationTime": "86400", 
		"AdvanceLoadTimeInSeconds": "180",
		"LoadPresentation": True, 
		"IsUploadAutomatic": True, 
		"AutoStart": True, 
		"AutoStop": True}

	url = (schedule_api)
	sched_post = requests.post(url, headers = headers, data = json.dumps(payload), verify = False)
	sched_post.raise_for_status()

	jsonData = sched_post.json()
	live_video_schedule_id = jsonData["Id"]

	#url2 = (schedule_api + "('"+ live_video_schedule_id + "')/Recurrences")
	#payload2 = {"StartRecordDateTime": time_from_now, "RecurrencePattern": "None", "RecordDuration": int(duration*60000)}

	#live_video_recurrence_post = requests.post(url2, headers = headers, data = json.dumps(payload2), verify = False)
	#live_video_recurrence_post.raise_for_status()

	return live_video_schedule_id


def get_mosaic_device_id():
	schedule_id = get_a_schedule_id("Mosaic Schedule (Automated)")

	url = (schedule_api + "('" + schedule_id + "')")

	get_schedule = requests.get(url, headers=headers, verify=False)
	assert get_schedule.status_code == 200, "Can't retrieve that Schedule?!"

	jsonData = get_schedule.json()
	mosaic_device_id = jsonData.get("DeviceId")

	return mosaic_device_id


def create_mosaic_schedule(time_from_now=m5, duration=10):

	device_id = get_mosaic_device_id()

	my_folder_id = get_a_folder_id("Scheduler")

	module_id = get_a_module_id("Mosaic Module")

	user_id = get_user_profile_id("Mosaic Tester")

	payload = {"Name": "Mosaic Test Schedule (WebAPI)",
		"Description": "Mosaic Schedule via WebAPI", 
		"DeviceId": device_id, 
		"ScheduleTemplateId": "10653d78ad54416d9a36cc56544b06cd",
		"TitleType": "ScheduleNameAndNumber", 
		"FolderId": my_folder_id,
		"UserProfileId": user_id,
		"CreatePresentation": True, 
		"AdvanceCreationTime": "0", 
		"AdvanceLoadTimeInSeconds": "0",
		"LoadPresentation": True, 
		"IsUploadAutomatic": True, 
		"AutoStart": True, 
		"AutoStop": True}


	url = (schedule_api)
	sched_post = requests.post(url, headers = headers, data = json.dumps(payload), verify = False)
	sched_post.raise_for_status()

	
	jsonData = sched_post.json()
	mosaic_schedule_id = jsonData["Id"]
	

	#Step 2 - Append a one-time only recurrence to the schedule we just created.

	url2 = (schedule_api + "('"+ mosaic_schedule_id + "')/Recurrences")
	payload2 = {"StartRecordDateTime": time_from_now, "RecurrencePattern": "None", "RecordDuration": int(duration*60000)}

	mosaic_recurrence_post = requests.post(url2, headers = headers, data = json.dumps(payload2), verify = False)
	mosaic_recurrence_post.raise_for_status()
	return mosaic_schedule_id


def add_module_to_mosaic_schedule():
	schedule_id = get_a_schedule_id("Mosaic Test Schedule (WebAPI)")

	module_id = get_a_module_id("Mosaic Module")

	mod_post_url = (modules_api + "('" + module_id + "')/AddAssociation")
	mod_payload = {"MediasiteId": schedule_id}

	mod_post = requests.post(mod_post_url, headers=headers, data=json.dumps(mod_payload), verify=False)
	mod_post.raise_for_status()

def delete_robot_mosaic_schedule():
	delete_schedule("Mosaic Test Schedule (WebAPI)")



def get_schedule_start_and_end_times(schedule_name):
	scheudle_id = get_a_scheudle_id(name=schedule_name)

	url = (schedule_api + "('" + schedule_id +"')")

	start_end_times = requests.get(url, headers=headers, json = {"key": "value"}, verify = False)

	"""TO BE CONTINUED - WE NEED A RECURRENCE TO GET THE START/END TIMES"""


	#return start_end_times.json()['']

#With very little effort, the same functions below can be done with Hardware Recorders too!
def get_recorders_scheduled_start_end_times(recorder_name):
	recorder_id = get_a_recorder_id(rec_name=recorder_name)

	url = (recorders_api + ("('" + recorder_id + "')/ScheduledRecordingTimes"))

	get_recorder_schedule_times = requests.get(url, headers=headers, json={"key": "value"}, verify=False)

	return get_recorder_schedule_times.json()#['StartTime'], get_recorder_start_and_end_times.json()['EndTime']


def recorder_sitrep(rec_name):
	rec_id = get_a_recorder_id(rec_name)
	url = (recorders_api + "/('" + rec_id + "')/ExtendedStatus")

	rec_ex_status = requests.get(url, headers = headers, json = {"key": "value"}, verify = False)
	assert rec_ex_status.status_code == 200, "Can't GET the ExtendedStatus via Recorder API endpoint?!"

	return rec_ex_status.json()['RecorderState'], rec_ex_status.json()['SystemState']

def recorder_sitrep2(rec_name):
	rec_id = get_a_recorder_id(rec_name)
	url = (recorders_api + "/('" + rec_id + "')/ExtendedStatus")

	rec_ex_status = requests.get(url, headers = headers, json = {"key": "value"}, verify = False)
	assert rec_ex_status.status_code == 200, "Can't GET the ExtendedStatus via Recorder API endpoint?!"

	return rec_ex_status.json()['RecorderState'], rec_ex_status.json()['SystemState']

def recorder_sync(rec_name):
	rec_id = get_a_recorder_id(rec_name)
	url = (recorders_api + "/('" + rec_id + "')/SyncSchedules")

	sync_post = requests.post(url, headers = headers, json = {"key": "value"}, verify = False)
	assert sync_post.status_code == 204, "Can't SYNC schedules via Recorder API endpoint?!"

def recorder_start(rec_name):
	rec_id = get_a_recorder_id(rec_name)
	url = (recorders_api + "/('" + rec_id + "')/Start")

	start_post = requests.post(url, headers = headers, json = {"key": "value"}, verify = False)
	assert start_post.status_code == 204, "Can't START recording on Recorder via API endpoint?!"

def recorder_pause(rec_name):
	rec_id = get_a_recorder_id(rec_name)
	url = (recorders_api + "/('" + rec_id + "')/Pause")

	pause_post = requests.post(url, headers = headers, json = {"key": "value"}, verify = False)
	assert pause_post.status_code == 204, "Can't PAUSE recording on Recorder via API endpoint?!"

def recorder_resume(rec_name):
	rec_id = get_a_recorder_id(rec_name)
	url = (recorders_api + "/('" + rec_id + "')/Resume")

	resume_post = requests.post(url, headers = headers, json = {"key": "value"}, verify = False)
	assert resume_post.status_code == 204, "Can't RESUME recording on Recorder via API endpoint?!"

def recorder_stop(rec_name):
	rec_id = get_a_recorder_id(rec_name)
	url = (recorders_api + "/('" + rec_id + "')/Stop")

	stop_post = requests.post(url, headers = headers, json = {"key": "value"}, verify = False)
	assert stop_post.status_code == 204, "Can't STOP recording on Recorder via API endpoint?!"



def get_current_preso_id_from_recorder(rec_name):
	rec_id = get_a_recorder_id(rec_name)

	url = (recorders_api + "('" + rec_id + "')" + "/CurrentPresentationMetadata")

	get_current_preso = requests.get(url, headers=headers, verify=False)
	assert get_current_preso.status_code == 200, "Can't hit 'CurrentPresentationMetadata' endpoint for that Recorder!"
	jsonData = get_current_preso.json()

	preso_id = jsonData["PresentationId"]
	return preso_id
	#for result in get_current_preso.json()['value']:
	#	if result["PresentationId"]:
	#		preso_id = result["Id"]
	#		return my_rec_id

def create_many_channels(number_of_channels):
	i = 0
	while i < int(number_of_channels):
		create_mediasite_channel("Channel " + str(i))
		i += 1


#This function will reset a Room's settings so that it is no longer associated with a Device or Room Configuration
# PATCH https://daily7x.sofoqa.net/mediasite/api/v1/Rooms('7908f35c5f194a47bb87682aa5b04e2152')
# {
#  "DeviceConfigurations": []
# }
#
#

def update_preso_duration(preso_title, new_value):
	preso_id = get_a_preso_id(title=preso_title)

	url = (preso_api + "('" + preso_id + "')")

	payload = {"Duration": new_value}

	duration_patch = requests.patch(url, headers=headers, data = json.dumps(payload), verify=False)
	assert duration_patch.status_code == 201, "WTF happened"


def get_presentations_with_long_duration():
    
    url = (preso_api + "?$top=1000")
    # OData filter for duration greater than 3 hours (10800 seconds)
    params = {
        "$filter": "Duration gt 360"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        presentations = response.json().get("value", [])
        if not presentations:
            print("No presentations found with duration greater than 3 hours.")
        else:
            for presentation in presentations:
                if 'Duration' in presentation:
                    title = presentation.get('Title', 'No Title')
                    duration = presentation.get('Duration', 'No Duration')
                    print(f"Title: {title}, Duration: {duration}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")