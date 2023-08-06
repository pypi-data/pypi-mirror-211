# XPVI

 Cross Platform Video Info
Get and save custom system-wide variables "to" a usb video device or filepath.
Also works with audio devices, very useful for saving calibration data.
Can also get a device index from it's name and vice-versa.



# Install

You will get an error if not admin,

but assuming you are an admin...

 => pip install XPVI



# Docs

 => XPVI(.bat or .sh)

...

syntax:
v* (get_all_video_devices)
a* (get_all_audio_devices)
v2i name (get_id_from_video_device)
a2i name (get_id_from_audio_device)
i2v id (get_video_device_from_id)
i2a id (get_audio_device_from_id)
set name key value (set_value)
set name key "NULL" (delete_key)
get name key (get_value)
get name "ALL" (get_values)



# Error Handling

 Not everyone has FFMPEG, but it's required for this to work.

So in every app that calls the XPVI cli (which is the only official way to interface with it),

it should first call XPVI itself and check if the word "syntax" is contained 

(case may change in the future, so check should be case-insensitive)...

If it contains it, there were no errors.

Otherwise, there was an error in the installation 

(maybe FFMPEG is missing for example, but we can't be sure)

and so we need to show a message box with the XPVI command's output.



# Example

 => XPVI.bat v*

...

[(0, 'c922 Pro Stream Webcam'), (1, 'OBS Virtual Camera')]



Now we know that 'c922 Pro Stream Webcam' is our video device...



=> XPVI.bat v2i "c922 Pro Stream Webcam"

...

0



INDEX = XPVI command output



#Great! We finally have a way to use a specific camera with opencv!

cap = cv2.VideoCapture(INDEX) 



... (INSERT CAMERA CALIBRATION CODE) ...



=> XPVI.bat set "c922 Pro Stream Webcam" fx (INSERT FOCAL X DATA)

...



=> XPVI.bat get "c922 Pro Stream Webcam" fx

...

(INSERT FOCAL X DATA)
