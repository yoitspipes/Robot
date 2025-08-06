***Settings***
Documentation  Recorder Express Web UI test for ad-hoc Display recording
Library  ../Resources/rec_exp_runner.py


*** Variables ***
${REMOTE_URL}    http://127.0.0.1:4723


*** Test Cases ***
Launch Recorder Web Interface And Login
	rec_exp_runner.launch_recorder_web  localhost

Create New Ad-Hoc Presentation
	rec_exp_runner.new_local_preso  Recorder Express Display Capture Robot Test  MP4 Max Quality

Verify State Is Idle
	rec_exp_runner.check_recorder_state  Idle
	BuiltIn.Sleep  2s

Start Recording Presentation
	rec_exp_runner.start_recording_ui  ${30}

Verify State Is Recording
	rec_exp_runner.check_recorder_state  Recording

Add A Chapter
	rec_exp_runner.add_chapter

Perform Pause
	rec_exp_runner.pause_recording_ui  ${5}

Verify State Is Paused
	rec_exp_runner.check_recorder_state  Paused

Perform Resume
	rec_exp_runner.resume_recording_ui  ${5}

Verify State Is Back To Recording
	rec_exp_runner.check_recorder_state  Recording

Add Another Chapter
	rec_exp_runner.add_chapter

Stop Recording After 10 More Seconds
	BuiltIn.Sleep  10s
	rec_exp_runner.stop_recording_ui

Verify State Returns To Idle
	rec_exp_runner.check_recorder_state  Idle