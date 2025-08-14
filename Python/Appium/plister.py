import plistlib
import os
import pprint

# Function to read and display a .plist file
def read_plist(file_path):
    try:
        with open(file_path, 'rb') as plist_file:
            # Load the .plist file
            plist_data = plistlib.load(plist_file)
            
            # Pretty-print the .plist content
            print("Contents of the .plist file:")
            pprint.pprint(plist_data)
    except Exception as e:
        print(f"Error reading .plist file: {e}")

# Specify the path to the .plist file
plist_file_path = "/Users/sqa/Desktop/Python/Info.plist"  # Replace with the actual file path

# Call the function
#read_plist(plist_file_path)



# Original Info.plist data
plist_data = {
    'CFBundleIconName': 'AppIcon',
    'CFBundleName': 'Mediasite Mosaic',
    'LSMinimumSystemVersion': '10.15',
    'CFBundleDevelopmentRegion': 'en',
    'CFBundleInfoDictionaryVersion': '6.0',
    'CFBundlePackageType': 'APPL',
    'CFBundleSignature': '????',
    'NSHumanReadableCopyright': '${AuthorCopyright:HtmlEncode}',
    'NSPrincipalClass': 'NSApplication',
    'NSMainStoryboardFile': 'Main',
    'NSCameraUsageDescription': 'The app records and displays video from your camera.',
    'NSMicrophoneUsageDescription': 'The app records audio and displays audio levels from your microphone.',
    'UIAppFonts': ['glyphicons-basic-regular.otf'],
    'ATSApplicationFontsPath': 'fonts',
    'CFBundleURLTypes': [
        {
            'CFBundleURLSchemes': ['x-com-sofo-desktoprecorder-2', 'mediasitecapture'],
            'CFBundleURLName': 'com.Mediasite.Capture',
            'CFBundleTypeRole': 'Viewer'
        }
    ],
    'LSApplicationCategoryType': 'public.app-category.video',
    'CFBundleIdentifier': 'com.sonicfoundry.mediasite.capture',
    'CFBundleShortVersionString': '2.4.109',
    'CFBundleVersion': '2.4.109',
    'ITSAppUsesNonExemptEncryption': False,
    'CFBundleDisplayName': 'Mediasite Mosaic',
    'CFBundleLocalizations': ['en', 'ja'],
    'CFBundleExecutable': 'Mediasite Mosaic',
    'BuildMachineOSBuild': '21E258',
    'DTCompiler': 'com.apple.compilers.llvm.clang.1_0',
    'DTPlatformBuild': '13F100',
    'DTSDKBuild': '21E258',
    'DTPlatformName': 'macosx',
    'DTPlatformVersion': '12.3',
    'DTSDKName': 'macosx12.3',
    'DTXcode': '1340',
    'DTXcodeBuild': '13F100',
    'MonoBundleExecutable': 'Mediasite Mosaic.exe'
}

# Add recommended changes
plist_data.update({
    "NSScreenCaptureUsageDescription": "The app records your screen for presentation purposes.",
    "NSCameraUseContinuityCameraDeviceType": True,
    "LSBackgroundOnly": False,
    "NSHighResolutionCapable": True
})

# File path to save the updated Info.plist
output_directory = "/Users/sqa/Desktop/Python"
output_file_path = os.path.join(output_directory, "Updated_Info.plist")

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Write the updated Info.plist to the specified location
def update_plist_file():
	with open(output_file_path, 'wb') as updated_plist_file:
		plistlib.dump(plist_data, updated_plist_file)
		print(f"Updated Info.plist saved to: {output_file_path}")