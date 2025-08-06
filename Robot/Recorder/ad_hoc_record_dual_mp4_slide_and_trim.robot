***Settings***
Documentation  Recorder Web UI test for ad-hoc dual mp4 and slide recording and trim
Library  ../Resources/recorder_cut_trim.py


*** Variables ***
${REMOTE_URL}    http://127.0.0.1:4723


*** Test Cases ***
Launch Recorder Web Interface And Login
	recorder_cut_trim.launch_recorder_web

Create New Ad-Hoc Presentation
	recorder_cut_trim.new_local_preso  Dual Video MP4 and Slides Robot Test  2 video 1 slide

Verify State Is Idle
	recorder_cut_trim.check_recorder_state  Idle
	BuiltIn.Sleep  2s

Start Recording Presentation
	recorder_cut_trim.start_recording_ui  ${30}

Verify State Is Recording
	recorder_cut_trim.check_recorder_state  Recording

Add A Chapter
	recorder_cut_trim.add_chapter

Perform Pause
	recorder_cut_trim.pause_recording_ui  ${5}

Verify State Is Paused
	recorder_cut_trim.check_recorder_state  Paused

Perform Resume
	recorder_cut_trim.resume_recording_ui  ${5}

Verify State Is Back To Recording
	recorder_cut_trim.check_recorder_state  Recording

Add Another Chapter
	recorder_cut_trim.add_chapter

Stop Recording After 10 More Seconds
	BuiltIn.Sleep  10s
	recorder_cut_trim.stop_recording_ui

Verify State Returns To Idle
	recorder_cut_trim.check_recorder_state  Idle

Navigate To Presentations Page
	recorder_cut_trim.nav_presos_pg

Find Recorded Presentation And Perform TRIM
	recorder_cut_trim.preso_trim  Dual Video MP4 and Slides Robot Test

Find Trimmed Presentation And Check Playback
	recorder_cut_trim.check_preso_playback  Dual Video MP4 and Slides Robot Test(Trim)

Delete Trimmed Presentation
	recorder_cut_trim.delete_preso  Dual Video MP4 and Slides Robot Test(Trim)

Delete Original Presentation
	recorder_cut_trim.delete_preso  Dual Video MP4 and Slides Robot Test


Teardown Test Session
	Teardown Actions

*** Keywords ***
Teardown Actions
	recorder_cut_trim.terminate
