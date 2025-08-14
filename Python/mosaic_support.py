import sqlite3
import os
import getpass

user = getpass.getuser()


"""For TechSupport in rare cases where some db cleansing is necessary"""

db_path = ("/Users/" + user + "/Library/Containers/com.sonicfoundry.mediasite.capture/Data/Library/Application Support/Sonic Foundry/Mediasite Mosaic/AppState.db3")
#db_path = (os.getcwd() + "/" + "AppState.db3")
#db_path = ("/Users/sqa/Library/Containers/com.sonicfoundry.mediasite.capture/Data/Library/Application Support/Sonic Foundry/Mediasite Mosaic/AppState.db3")

print("When ready, type: \n fix_it()")

def create_connection(db_path):
	conn = None
	try:
		conn = sqlite3.connect(db_path)
	except Error as e:
		print(e)

	return conn

conn = create_connection(db_path=db_path)
 
def delete_zero_duration_recordings():
	sql = ('''DELETE FROM persistedpresentation WHERE Duration = 0''')
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()

#Used in cases where there might be a mismatch between us and Mac's Keychain creds
def reset_mvp():
	sql = ('''DELETE FROM persistedmediasiteserver''')
	sql2 = ('''DELETE FROM persistedsetting WHERE Name = "ActiveMVPServerConnection"''')

	cur = conn.cursor()
	cur.execute(sql)
	cur.execute(sql2)

	conn.commit()
	print("MVP connection has been reset.  Please re-register via My Mediasite using Safari.")


def fix_it():
	delete_zero_duration_recordings()
	print("Corrupt recording(s) have been removed.\n ")
