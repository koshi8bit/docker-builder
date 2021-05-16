import shutil
import os, sys, time
import glob
import subprocess
from dotenv import load_dotenv

import os
import tempfile

file_list = """
.env
Dockerfile
main.py
requirements.txt
telegram_my.py
udpipe.py
udpipe_requests.py
"""

delete_later = []


def clear_folder():
    for filename in os.listdir(src_folder):
        file_path = os.path.join(src_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def copy_folder():
    for file in file_list.split('\n'):
        if file == "":
            continue
        shutil.copy(file, src_folder)


def run_script(text):
    # _, script_filename = tempfile.mkstemp()
    script_filename = 'script.tmp'
    with open(script_filename, 'w') as build_script_file:
        build_script_file.write(text)

    build_script_file.close()

    os.system(f'start /B /Wait "" {putty} -load "deb" -l {linux_login} -pw {linux_pass} -m {script_filename}')
    time.sleep(1)
    os.remove(script_filename)


if __name__ == '__main__':
    load_dotenv()
    src_folder = os.getenv('src_folder')
    clear_folder()
    copy_folder()

    linux_login = os.getenv('dest_login')
    linux_pass = os.getenv('dest_pass')

    putty = os.getenv('putty')
    putty_profile = os.getenv('putty_profile')
    clear_script = os.getenv('clear_script')

    dest_folder = os.getenv('dest_folder')

    run_script(f"""
cd {dest_folder}
rm *
""")

    # os.system(f'start /B /Wait "" {putty} -load "deb" -l {linux_login} -pw {linux_pass} -m {clear_script}')

    pscp = os.getenv('pscp')
    dest_ip = os.getenv('dest_ip')
    dest_port = os.getenv('dest_port')
    os.system(f'start /B /Wait "" {pscp} -P {dest_port} -r -pw {linux_pass} {src_folder+"/*"} {linux_login}@{dest_ip}:{dest_folder}')

    container_name = os.getenv('container_name')
    dockerhub_login = os.getenv('dockerhub_login')

    run_script(f"""
cd {dest_folder}
docker build -t {container_name} .
echo {os.getenv('dockerhub_pass')} | docker login --username {dockerhub_login} --password-stdin
docker tag {container_name} {dockerhub_login}/{container_name}
docker push {dockerhub_login}/{container_name}
""")
