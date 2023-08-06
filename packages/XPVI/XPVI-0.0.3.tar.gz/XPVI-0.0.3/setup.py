from setuptools import setup, find_packages
import codecs
import sys
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'Get and save custom variables "to" a usb video device'
LONG_DESCRIPTION = 'Cross Platform Video Info, \n' + \
'Get and save custom system-wide variables "to" a usb video device or filepath, \n' + \
'Also works with audio devices, very useful for saving calibration data, \n' + \
'Can also get a device index from it\'s name and vice-versa'

def install_package():
    with open(os.path.join(
        os.path.abspath(os.path.join(sys.executable, os.pardir)
    ), 'XPVI.py'), 'w') as fp:
        fp.write('import os\nimport sys\nimport re\nfrom subprocess import Popen, PIPE, STDOUT\ntry:\n    from subprocess import CREATE_NO_WINDOW\nexcept:\n    CREATE_NO_WINDOW = None\n\nscripts_dir = os.path.dirname(\n    os.path.realpath(\n        sys.executable\n    )\n)\n\ndef __raw_video_device_data():\n    has_ffmpeg = True\n    try:\n        proc = Popen([\'ffmpeg\', \'-version\'],\n                     creationflags=CREATE_NO_WINDOW, stderr=STDOUT,\n                     stdout=PIPE)\n    except:\n        try:\n            proc = Popen([\'ffmpeg\', \'-version\'],\n                         stderr=STDOUT, stdout=PIPE)\n        except:\n            has_ffmpeg = False\n    if not has_ffmpeg:\n        raise RuntimeError(\'ffmpeg not found\')\n    formats = [\n        \'alsa\',\n        \'android_camera\',\n        \'avfoundation\',\n        \'bktr\',\n        \'decklink\',\n        \'dshow\',\n        \'fbdev\',\n        \'gdigrab\',\n        \'iec61883\',\n        \'jack\',\n        \'kmsgrab\',\n        \'lavfi\',\n        \'libcdio\',\n        \'libdc1394\',\n        \'openal\',\n        \'oss\',\n        \'pulse\',\n        \'sndio\',\n        \'video4linux2\',\n        \'v4l2\',\n        \'vfwcap\',\n        \'x11grab\',\n    ]\n    raw_video_device_data = \'\'\n    for fmt in formats:\n        try:\n            raw_video_device_data += Popen(\n                [\n                    \'ffmpeg\',\n                    \'-f\',\n                    fmt,\n                    \'-list_devices\',\n                    \'true\',\n                    \'-i\',\n                    \'x\'\n                ],\n                creationflags=CREATE_NO_WINDOW,\n                stderr=STDOUT, stdout=PIPE\n            ).communicate()[0].decode(\'utf-8\') + \'\\n\'\n        except:\n            raw_video_device_data += Popen(\n                [\n                    \'ffmpeg\',\n                    \'-f\',\n                    fmt,\n                    \'-list_devices\',\n                    \'true\',\n                    \'-i\',\n                    \'x\'\n                ],\n                stderr=STDOUT, stdout=PIPE\n            ).communicate()[0].decode(\'utf-8\') + \'\\n\'\n    return raw_video_device_data\n\ndef __find_devices(kind):\n    matches = re.findall(r\'"(.+)"\\s+\\(\' + kind + \'\\)\', __raw_video_device_data())\n    return matches\n\ndef get_all_video_devices():\n    return list(enumerate(__find_devices(\'video\')))\n\ndef get_all_audio_devices():\n    return list(enumerate(__find_devices(\'audio\')))\n\ndef get_id_from_video_device(name):\n    ID = -1\n    for device in get_all_video_devices():\n        if device[1] == name:\n            ID = device[0]\n            break\n    return ID\n\ndef get_id_from_audio_device(name):\n    ID = -1\n    for device in get_all_audio_devices():\n        if device[1] == name:\n            ID = device[0]\n            break\n    return ID\n\ndef get_video_device_from_id(ID):\n    name = ""\n    for device in get_all_video_devices():\n        if device[0] == ID:\n            name = device[1]\n            break\n    return name\n\ndef get_audio_device_from_id(ID):\n    name = ""\n    for device in get_all_audio_devices():\n        if device[0] == ID:\n            name = device[1]\n            break\n    return name\n\nglobal env\nenv = {}\n\ndef save_env():\n    global env\n    if os.path.exists(os.path.join(scripts_dir, \'XPVI.env\')):\n        os.remove(os.path.join(scripts_dir, \'XPVI.env\'))\n    with open(os.path.join(scripts_dir, \'XPVI.env\'), \'w\') as fp:\n        fp.write(str(env))\n\ndef load_env():\n    global env\n    if not os.path.exists(os.path.join(scripts_dir, \'XPVI.env\')):\n        save_env()\n    with open(os.path.join(scripts_dir, \'XPVI.env\'), \'r\') as fp:\n        env = eval(fp.read())\n\nload_env()\n\nif __name__ == \'__main__\':\n    __raw_video_device_data()\n    if len(sys.argv) == 2 and sys.argv[1] == \'v*\':\n        print(get_all_video_devices())\n    elif len(sys.argv) == 2 and sys.argv[1] == \'a*\':\n        print(get_all_audio_devices())\n    elif len(sys.argv) == 3 and sys.argv[1] == \'v2i\':\n        if os.path.exists(sys.argv[2]):\n            print(sys.argv[2])\n        else:\n            print(str(get_id_from_video_device(sys.argv[2])))\n    elif len(sys.argv) == 3 and sys.argv[1] == \'a2i\':\n        if os.path.exists(sys.argv[2]):\n            print(sys.argv[2])\n        else:\n            print(str(get_id_from_audio_device(sys.argv[2])))\n    elif len(sys.argv) == 3 and sys.argv[1] == \'i2v\':\n        if os.path.exists(sys.argv[2]):\n            print(sys.argv[2])\n        else:\n            try:\n                print(get_video_device_from_id(int(sys.argv[2])))\n            except:\n                pass\n    elif len(sys.argv) == 3 and sys.argv[1] == \'i2a\':\n        if os.path.exists(sys.argv[2]):\n            print(sys.argv[2])\n        else:\n            try:\n                print(get_audio_device_from_id(int(sys.argv[2])))\n            except:\n                pass\n    elif len(sys.argv) == 5 and sys.argv[1] == \'set\':\n        ID = str(get_id_from_video_device(sys.argv[2]))\n        if os.path.exists(sys.argv[2]):\n            ID = sys.argv[2]\n        if ID == \'-1\':\n            ID = str(get_id_from_audio_device(sys.argv[2]))\n        if ID == \'-1\':\n            print(\'Error@DeviceName\')\n        elif sys.argv[3] is None or len(sys.argv[3]) == 0:\n            print(\'Error@Key\')\n        elif str(sys.argv[4]) == \'NULL\':\n            env.pop(sys.argv[2] + \'\\\\\' + sys.argv[3])\n            save_env()\n        else:\n            env[sys.argv[2] + \'\\\\\' + sys.argv[3]] = str(sys.argv[4])\n            save_env()\n    elif len(sys.argv) == 4 and sys.argv[1] == \'get\':\n        ID = str(get_id_from_video_device(sys.argv[2]))\n        if os.path.exists(sys.argv[2]):\n            ID = sys.argv[2]\n        if ID == \'-1\':\n            ID = str(get_id_from_audio_device(sys.argv[2]))\n        if ID == \'-1\':\n            print(\'Error@DeviceName\')\n        elif sys.argv[3] is None or len(sys.argv[3]) == 0:\n            print(\'Error@Key\')\n        else:\n            load_env()\n            if sys.argv[3] == \'ALL\':\n                tmp1 = [k for k in env if k.startswith(sys.argv[2] + \'\\\\\')]\n                tmp2 = {}\n                for tmp in tmp1:\n                    tmp2[tmp] = env[tmp]\n                print(str(tmp2))\n            else:\n                print(str(env[sys.argv[2] + \'\\\\\' + sys.argv[3]]))\n    else:\n        print(\'syntax:\')\n        print(\'v* (get_all_video_devices)\')\n        print(\'a* (get_all_audio_devices)\')\n        print(\'v2i name (get_id_from_video_device)\')\n        print(\'a2i name (get_id_from_audio_device)\')\n        print(\'i2v id (get_video_device_from_id)\')\n        print(\'i2a id (get_audio_device_from_id)\')\n        print(\'set name key value (set_value)\')\n        print(\'set name key "NULL" (delete_key)\')\n        print(\'get name key (get_value)\')\n        print(\'get name "ALL" (get_values)\')\nelse:\n    print("Error: Apps should use the XPVI cli")\n')
    with open(os.path.join(
        os.path.abspath(os.path.join(sys.executable, os.pardir)
    ), 'XPVI.bat'), 'w', newline='\r\n') as fp:
        fp.write('@echo off\npushd "%~dp0"\npython3 --version >nul 2>&1 && (\n    python3 XPVI.py %*\n) || (\n    python XPVI.py %*\n)\npopd')
    with open(os.path.join(
        os.path.abspath(os.path.join(sys.executable, os.pardir)
    ), 'XPVI.sh'), 'w', newline='\n') as fp:
        fp.write('#!/bin/bash\npushd $(dirname "$BASH_SOURCE") > /dev/null\nif command -v python3 &> /dev/null\nthen\n    python3 XPVI.py "${@:1}"\nelse\n    python XPVI.py "${@:1}"\nfi\npopd > /dev/null\n')
    setup(
        name="XPVI",
        version=VERSION,
        author="Karrson Heumann",
        author_email="<mail@example.com>",
        description=DESCRIPTION,
        long_description_content_type="text/markdown",
        long_description=long_description,
        packages=find_packages(),
        install_requires=[],
        keywords=['python', 'video', 'audio', 'camera', 'microphone', 'data'],
        classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: Unix",
            "Operating System :: Microsoft :: Windows",
        ]
    )

is_admin = False
AdminTest = 'admin_test.tmp'
if os.name == 'nt':
    AdminTest = 'C:\\' + AdminTest
    try:
        if os.path.exists(AdminTest):
            os.remove(AdminTest)
        with open(AdminTest, 'w') as fp:
            fp.write(AdminTest)
        if os.path.exists(AdminTest):
            is_admin = True
            os.remove(AdminTest)
    except:
        pass
else:
    AdminTest = '/' + AdminTest
    try:
        if os.path.exists(AdminTest):
            os.remove(AdminTest)
        with open(AdminTest, 'w') as fp:
            fp.write(AdminTest)
        if os.path.exists(AdminTest):
            is_admin = True
            os.remove(AdminTest)
    except:
        pass

if not is_admin:
    AdminError = 'You must be an admin to install this package.'
    try:
        raise PermissionError(AdminError)
    except:
        raise Exception(AdminError)
else:
    install_package()
