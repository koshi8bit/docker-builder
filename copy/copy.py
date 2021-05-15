import shutil
import os
import glob
import subprocess


def execc(cmd):
    print(subprocess.check_output(cmd, shell=True))


files = """.env
Dockerfile
main.py
requirements.txt
telegram_my.py
udpipe.py
udpipe_requests.py"""

files = files.split('\n')
# dest_folder = r'Z:\06\go\books\to_linux'
dest_folder = 'to_linux'

for filename in os.listdir(dest_folder):
    file_path = os.path.join(dest_folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

for file in files:
    shutil.copy(file, dest_folder)

login = 'test'
passw = '11'

putty = r'"F:\home\koshi8bit\soft\windows\01_osnovnoe\ssh\putty\putty.exe"'
clear_script = r'F:\home\koshi8bit\work\05-nsu\06\go\books\copy\clear.sh'
os.system(f'start /B /Wait "" {putty} -load "deb" -l {login} -pw {passw} -m {clear_script}')
# execc(f'start /B /Wait "" {putty} -load "deb" -l {login} -pw {passw} -m {clear_script}')


pscp = r'"F:\home\koshi8bit\soft\windows\01_osnovnoe\ssh\putty\pscp.exe"'
src = r'".\to_linux\*"'
dest = '/home/test/mc/src'
os.system(f'start /B /Wait "" {pscp} -P 2222 -r -pw {passw} {src} {login}@127.0.0.1:{dest}')
# execc(f'start /B /Wait "" {pscp} -P 2222 -r -pw {passw} {src} {login}@127.0.0.1:{dest}')

build_script = r'F:\home\koshi8bit\work\05-nsu\06\go\books\copy\build.sh'
os.system(f'start /B /Wait "" {putty} -load "deb" -l {login} -pw {passw} -m {build_script}')
# execc(f'start /B /Wait "" {putty} -load "deb" -l {login} -pw {passw} -m {build_script}')
