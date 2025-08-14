import sqlite3
import os

"""Mediasite Mosaic python script for interfacing with the sqlite DB file"""
db_path = ("/Users/sqa/Library/Containers/com.sonicfoundry.mediasite.capture/Data/Library/Application Support/Sonic Foundry/Mediasite Mosaic/AppState.db3")

#old_db_path = /Users/sqa/Library/Containers/com.sonicfoundry.mediasite.capture/Data/Library/Application Support/Sonic Foundry/Mediasite Mosaic

def create_connection(db_path):
	conn = None
	try:
		conn = sqlite3.connect(db_path)
	except Error as e:
		print(e)

	return conn

conn = create_connection(db_path=db_path)


def get_mosaic_preso_id(preso_name):
	sql = ('''SELECT PresentationId FROM persistedpresentation WHERE Name = ''' + preso_name)
	cur = conn.cursor()
	preso_id = cur.execute(sql)
	mosaic_preso_id = preso_id.fetchall()[0][0]
	return mosaic_preso_id

def check_preso_status(preso_name):

	mosaic_preso_id = get_mosaic_preso_id(preso_name)
	cur = conn.cursor()

	sql = ('''SELECT PublishAttemptCount, MostRecentJobProgress, Status FROM persistedpresentation WHERE PresentationId = ''' + "'" + mosaic_preso_id +"'")
	preso_status = cur.execute(sql)

	return (preso_status.fetchall())

def reset_publishing_status_for_preso(preso_name):
	
	mosaic_preso_id = get_mosaic_preso_id(preso_name)
	cur = conn.cursor()

	reset_pub_count = ('''UPDATE persistedpresentation SET PublishAttemptCount = 0 WHERE PresentationId = ''' + "'"+ mosaic_preso_id +"'")
	reset_pub_op = ('''UPDATE persistedpresentation SET CurrentJobType = 0 WHERE PresentationId = ''' + "'" + mosaic_preso_id + "'")
	reset_job_prog = ('''UPDATE persistedpresentation SET MostRecentJobProgress = 0 WHERE PresentationId = ''' + "'" + mosaic_preso_id + "'")
	reset_job_status = ('''UPDATE persistedpresentation SET Status = 4 WHERE PresentationId = ''' + "'" + mosaic_preso_id + "'")
	set_auto_upload = ('''UPDATE persistedpresentation SET IsUploadAutomatic = 1 WHERE PresentationId = ''' + "'" + mosaic_preso_id + "'")

	set_null_mvp_id = ('''UPDATE persistedpresentation SET MvpId = NULL WHERE PresentationId = ''' + "'" + mosaic_preso_id + "'")
	set_null_preso_id = ('''UPDATE persistedpresentation SET PresentationUrl = NULL WHERE PresentationId = ''' + "'" + mosaic_preso_id + "'")
	


	cur.execute(reset_pub_count)
	cur.execute(reset_pub_op)
	cur.execute(reset_job_prog)
	cur.execute(reset_job_status)
	cur.execute(set_auto_upload)
	cur.execute(set_null_preso_id)
	cur.execute(set_null_mvp_id)
	
	conn.commit()



def select_all_settings(conn):
	cur = conn.cursor()
	cur.execute("SELECT * FROM persistedsetting")

	rows = cur.fetchall()

	for row in rows:
		print(row)

debug_log = ('''INSERT INTO persistedsetting(Name, Value, ValueType, Id) VALUES("CaptureVerboseLogging", "True", "System.Boolean", 9)''')

def enable_debug_logging():
	cur = conn.cursor()
	cur.execute(debug_log)
	conn.commit()

def add_upload_chunk_size(size):
	cur = conn.cursor()
	sql = ('''INSERT INTO persistedsetting(Name, Value, ValueType) VALUES("UploadChunkSizeMB", ''' + str(size) + ''', "System.Int32")''')
	cur.execute(sql)
	conn.commit()

def change_upload_chunk_size(new_size):
	cur = conn.cursor()
	sql = ('''UPDATE "persistedsetting" SET Value = ''' + str(new_size) + ''' WHERE Name = "UploadChunkSizeMB"''')
	cur.execute(sql)
	conn.commit()

def delete_upload_chunk():
	cur = conn.cursor()
	sql = ('''DELETE FROM persistedsetting WHERE Name = "UploadChunkSizeMB"''')
	cur.execute(sql)
	conn.commit()


def delete_mvp_connection():
	sql1 = ('''DELETE FROM persisteduseraccount''')
	sql2 = ('''DELETE FROM persistedmediasiteserver''')
	sql3 = ('''DELETE FROM persistedsetting WHERE Name = "ActiveMVPServerConnection"''')
	cur = conn.cursor()
	cur.execute(sql1)
	cur.execute(sql2)
	cur.execute(sql3)
	conn.commit()

def disable_debug_logging():
	#def delete_row(table, column_name, column_value):
	#sql_delete = ("DELETE FROM " + table + " WHERE " + column_name + " = " + column_value)
	sql = '''DELETE FROM persistedsetting WHERE Name = "CaptureVerboseLogging"'''

	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()

def delete_all(table, conn):
	sql = ('''DELETE FROM ''' + table)

	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()

def delete_from(table, column, value, conn):
	sql = ('''DELETE FROM ''' + table + ''' WHERE ''' + column + ''' = ''' + "'" + value + "'")
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()

def select_all(table, conn):
	cur = conn.cursor()
	cur.execute("SELECT * FROM " + table)

	rows = cur.fetchall()

	for row in rows:
		print(row)

def select_where(table, where, conn):
	cur = conn.cursor()
	cur.execute('''SELECT * FROM ''' + table + ''' WHERE ''' + where)

	rows = cur.fetchall()

	for row in rows:
		print(row)

"""Sketchy db insert statement to allow Capture to record max resolution of Mac decice"""
custom_max_quality = ('''INSERT INTO persistedencodedstreamprofile(EncodedStreamType, Description, CodecFourCC, CodecProfile, CodecLevel, SampleRate, BitRate, VariableRate, MaxBitRate, RequiredEncodeCapacity, HexEncodedCodecPrivateData, NumChannels, BitDepth, BlockAlign, Width, Height, GopIntervalms, Progressive, Id) VALUES (1, 'H264,5500000 bps 2880x1800 30 fps', 'H264', 'Main', 4.0, 30, 5500000, 0, 5500000, 100, '00000001674D4028965603C0113F2FFE08000800A10000030001000003003C62A00029F6000053EC7F18E31500014FB000029F63F8C70ED09129C00000000168CA5352', 0, 0, 0, 2880, 1800, 2, 1, 1)''')
custom_max_quality2 = ('''INSERT INTO persistedencodedstreamprofile(EncodedStreamType, Description, CodecFourCC, CodecProfile, CodecLevel, SampleRate, BitRate, VariableRate, MaxBitRate, RequiredEncodeCapacity, HexEncodedCodecPrivateData, NumChannels, BitDepth, BlockAlign, Width, Height, GopIntervalms, Progressive, Id) VALUES (1, 'H264,5500000 bps 2880x1800 30 fps', 'H264', 'Main', 4.0, 30, 5500000, 0, 5500000, 100, '00000001674D4028965603C0113F2FFE08000800A10000030001000003003C62A00029F6000053EC7F18E31500014FB000029F63F8C70ED09129C00000000168CA5352', 0, 0, 0, 2880, 1800, 2, 1, 1)''')
restore_max_quality = (''' INSERT INTO persistedencodedstreamprofile(EncodedStreamType, Description, CodecFourCC, CodecProfile, CodecLevel, SampleRate, BitRate, VariableRate, MaxBitRate, RequiredEncodeCapacity, HexEncodedCodecPrivateData, NumChannels, BitDepth, BlockAlign, Width, Height, GopIntervalms, Progressive, Id) VALUES (1, 'H264,5500000 bps 1920x1080 30 fps', 'H264', 'Main', 4.0, 30, 5500000, 0, 5500000, 100, '00000001674D4028965603C0113F2FFE08000800A10000030001000003003C62A00029F6000053EC7F18E31500014FB000029F63F8C70ED09129C00000000168CA5352', 0, 0, 0, 1920, 1080, 2, 1, 7)''')
vertical_monitor = ('''INSERT INTO persistedencodedstreamprofile(EncodedStreamType, Description, CodecFourCC, CodecProfile, CodecLevel, SampleRate, BitRate, VariableRate, MaxBitRate, RequiredEncodeCapacity, HexEncodedCodecPrivateData, NumChannels, BitDepth, BlockAlign, Width, Height, GopIntervalms, Progressive, Id) VALUES (1, 'H264,5500000 bps 1080x1920 30 fps', 'H264', 'Main', 4.0, 30, 5500000, 0, 5500000, 100, '00000001674D4028965603C0113F2FFE08000800A10000030001000003003C62A00029F6000053EC7F18E31500014FB000029F63F8C70ED09129C00000000168CA5352', 0, 0, 0, 1080, 1920, 2, 1, 7)''')
custom_quality_480p = ('''UPDATE persistedencodedstreamprofile SET Description = 'H264,1500000 bps 480x720 30 fps', Height = 360, Width = 640 WHERE Id = 6''')
custom_screen_1440_900 = ('''UPDATE persistedencodedstreamprofile SET Description = 'H264,5500000 bps 1440x900 30 fps', Height = 900, Width = 1440 WHERE Id = 1''')
default_max = ('''UPDATE persistedencodedstreamprofile SET Description = 'H264,5500000 bps 1920x1080 30 fps', CodecFourCC = "H264", CodecProfile = "Main", Height = 1080, Width = 1920, SampleRate = 30, VariableRate=0, BitRate = 5500000, MaxBitRate = 5500000, GopIntervalms = 2 WHERE Id = 1''')
default_max2 = ('''UPDATE persistedencodedstreamprofile SET Description = 'H264,5500000 bps 1920x1080 30 fps', CodecFourCC = "H264", CodecProfile = "Main", Height = 720, Width = 1080, SampleRate = 30, VariableRate=0, BitRate = 3217000, MaxBitRate = 3217000, GopIntervalms = 2 WHERE Id = 2''')
bad_custom_quality1 = ('''UPDATE persistedencodedstreamprofile SET Description = 'H264,5500000 bps 144x90 30 fps', Height = 12, Width = 34 WHERE Id = 1''')
bad_custom_quality2 = ('''UPDATE persistedencodedstreamprofile SET Description = 'H264,5500000 bps 145x95 30 fps', Height = 16, Width = 56 WHERE Id = 2''')
bad_custom_quality3 = ('''UPDATE persistedencodedstreamprofile SET Description = 'H264,5500000 bps 147x97 30 fps', Height = 22, Width = 67 WHERE Id = 3''')

custom_max = ('''UPDATE persistedencodedstreamprofile SET Description = 'H264,3200000 bps 3000x2000 30 fps', Height = 1920, Width = 1080 WHERE Id = 1''')
custom_fps_720p = ('''UPDATE persistedencodedstreamprofile SET Description = 'H264,32170000 bps 1080x720 15 fps', SampleRate = 15.0 WHERE RequiredEncodeCapacity = 48''')
restore_default_fps_720 = ('''UPDATE persistedencodedstreamprofile SET Description = 'H264,3217000 bps 1080x720 30 fps', SampleRate = 30.0 WHERE RequiredEncodeCapacity = 48''')


#1440 900


def set_none_sources(conn):
	audio_sql = ('''UPDATE "persistedsetting" SET "Value" = "SFSilentSource" WHERE "Name" = "AudioRoutedDeviceId"''')
	vid1_sql = ('''UPDATE "persistedsetting" SET "Value" = "SFBlackSource" WHERE "Name" = "Video1RoutedDeviceId"''')
	vid2_sql = ('''UPDATE "persistedsetting" SET "Value" = "SFBlackSource" WHERE "Name" = "Video2RoutedDeviceId"''')

	cur = conn.cursor()
	cur.execute(audio_sql)
	cur.execute(vid1_sql)
	cur.execute(vid2_sql)
	conn.commit()
	print("All input devices set to 'None'")




def return_all_rows(table, conn):
	cur = conn.cursor()
	cur.execute('''SELECT * FROM ''' + table)

	rows = cur.fetchall()

	return rows


default_qualities = return_all_rows("persistedencodedstreamprofile", conn)
restore_qualities = ('''INSERT INTO persistedencodedstreamprofile(EncodedStreamType, Description, CodecFourCC, CodecProfile, CodecLevel, SampleRate, BitRate, VariableRate, MaxBitRate, RequiredEncodeCapacity, HexEncodedCodecPrivateData, NumChannels, BitDepth, BlockAlign, Width, Height, GopIntervalms, Progressive, Id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''')


def set_max_record_quality(quality):
	cur = conn.cursor()
	cur.execute(quality)
	conn.commit()


def restore_default_qualities(conn):
	delete_all("persistedencodedstreamprofile", conn)
	cur = conn.cursor()
	cur.executemany(restore_qualities, default_qualities)
	conn.commit()
	print("Original encoding profiles restored!")


def add_encoding_for_vertical_monitor():
	cur = conn.cursor()
	cur.execute(vertical_monitor)
	conn.commit()


def restore_default_max_quality():
	cur = conn.cursor()
	cur.execute(restore_max_quality)
	conn.commit()

def change_to_15fps_720p():
	cur = conn.cursor()
	cur.execute(custom_fps_720p)
	conn.commit()

def revert_to_30fps_720p():
	cur = conn.cursor()
	cur.execute(restore_default_fps_720)
	conn.commit()

def delete_custom_quality():
	delete_statement = '''DELETE FROM persistedencodedstreamprofile WHERE Id = 3'''

	cur = conn.cursor()
	cur.execute(delete_statement)	

def delete_default_max_quality():
	sql = '''DELETE FROM persistedencodedstreamprofile WHERE Id = 1'''

	cur = conn.cursor()
	cur.execute(sql)

def delete_default_max_quality_five():
	sql = '''DELETE FROM persistedencodedstreamprofile WHERE Id = 5'''

	cur = conn.cursor()
	cur.execute(sql)

def delete_default_max_quality_zero():
	sql = '''DELETE FROM persistedencodedstreamprofile WHERE Id = 0'''

	cur = conn.cursor()
	conn.execute(sql)

def delete_zero_duration_recordings():
	sql = ('''DELETE FROM persistedpresentation WHERE Duration = 0''')
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()

def delete_schedules():
	sql = ('''DELETE FROM persistedpresentation WHERE ScheduleId IS NOT null''')
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()

def set_custom_screen_1440_900():
	cur = conn.cursor()
	cur.execute(custom_screen_1440_900)
	conn.commit()

def set_custom_quality_480p():
	cur = conn.cursor()
	cur.execute(custom_quality_480p)
	conn.commit()

def set_bad_custom_qualities():
	cur = conn.cursor()
	cur.execute(bad_custom_quality1)
	cur.execute(bad_custom_quality2)
	cur.execute(bad_custom_quality3)
	conn.commit()

def modify_custom_camera_quality():
	cur = conn.cursor()
	cur.execute(custom_quality_480p)
	conn.commit()

def modify_quality(height, width, qid):
	cur = conn.cursor()
	custom_quality = ('''UPDATE persistedencodedstreamprofile SET Height = ''' + str(height) + ''', ''' + '''Width = ''' + str(width) + ''' WHERE Id = ''' + str(qid))
	cur.execute(custom_quality)
	conn.commit()

#def rename_media_files(preso_name, video1, video2):

#UPDATE persistedencodedstreamprofile SET Description = 'H264,1500000 bps 540x960 30 fps', Height = 540, Width = 960 WHERE Id = 3
#insert into persistedencodedstreamprofile(EncodedStreamType, Description, CodecFourCC, CodecProfile, CodecLevel, SampleRate, BitRate, VariableRate, MaxBitRate, RequiredEncodeCapacity, HexEncodedCodecPrivateData, NumChannels, BitDepth, BlockAlign, Width, Height, GopIntervalms, Progressive, Id)
#values(1, 'H264,5500000 bps 1920x1080 30 fps', 'H264', 'Main', 4.0, 30, 5500000, 0, 5500000, 100, '00000001674D4028965603C0113F2FFE08000800A10000030001000003003C62A00029F6000053EC7F18E31500014FB000029F63F8C70ED09129C00000000168CA5352', 0, 0, 0, 1920, 1080, 2, 1, 1)
#values(1, 'H264,5500000 bps 2880x1800 30 fps', 'H264', 'Main', 4.0, 30, 5500000, 0, 5500000, 100, '00000001674D4028965603C0113F2FFE08000800A10000030001000003003C62A00029F6000053EC7F18E31500014FB000029F63F8C70ED09129C00000000168CA5352', 0, 0, 0, 2880, 1800, 2, 1, 5)