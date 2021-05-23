import shutil
import os, sys, time
import glob
import subprocess
from dotenv import load_dotenv
import os
import tempfile
import argparse

parser = argparse.ArgumentParser(description="Flip a switch by setting a flag")
parser.add_argument('-p', '--push', action='store_true', help="Push to dockerhub")
parser.add_argument('-r', '--restart', action='store_true', help="Restart containers")
args = parser.parse_args()

delete_later = []


def restart():
    with open('restart.sh', 'r') as file:
        script = file.read()
        run_script(script)
    print('*** RESTART OK ***')


def build():
    run_script(f"""
cd {dest_folder}
docker build -t {container_name} .
docker tag {container_name} {dockerhub_login}/{container_name}
    """)
    print('*** BUILD OK ***')


def push():
    run_script(f"""
echo {os.getenv('dockerhub_pass')} | docker login --username {dockerhub_login} --password-stdin
docker push {dockerhub_login}/{container_name}
        """)
    print('*** PUSH OK ***')


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
    print('*** CLEAR OK ***')


def copy_folder():
    with open('files.txt', 'r') as fff:
        file_list = fff.read().split('\n')
        for f in file_list:
            if f == "":
                continue
            shutil.copy('../' + f, src_folder)
    print('*** COPY TMP OK ***')


def run_script(text):
    # _, script_filename = tempfile.mkstemp()
    script_filename = 'script.tmp'
    with open(script_filename, 'w') as build_script_file:
        build_script_file.write(text)

    build_script_file.close()
    cmd = f'start /B /Wait "" {putty} -ssh {dest_ip} -P {dest_port} -l {linux_login} -pw {linux_pass} -m {script_filename}'
    # cmd = f'start /B /Wait "" {putty} -load "deb" -l {linux_login} -pw {linux_pass} -m {script_filename}'
    # print('running', cmd)
    os.system(cmd)

    time.sleep(1)
    os.remove(script_filename)


if __name__ == '__main__':
    load_dotenv()

    dest_ip = os.getenv('dest_ip')
    dest_port = os.getenv('dest_port')

    src_folder = os.getenv('src_folder')
    src_folder = f'../{src_folder}'

    linux_login = os.getenv('dest_login')
    linux_pass = os.getenv('dest_pass')

    putty = os.getenv('putty')
    putty_profile = os.getenv('putty_profile')
    clear_script = os.getenv('clear_script')

    dest_folder = os.getenv('dest_folder')

#     run_script(f'''
# top
# ping google.com
#     ''')
#     sys.exit()

    clear_folder()
    copy_folder()


    with open('clear.sh', 'r') as file:
        script = file.read()
        script = script.replace('{dest_folder}', dest_folder)
        run_script(script)

    pscp = os.getenv('pscp')
    os.system(f'start /B /Wait "" {pscp} -P {dest_port} -r -pw {linux_pass} {src_folder+"/*"} {linux_login}@{dest_ip}:{dest_folder}')
    print('*** COPY REMOTE OK ***')

    container_name = os.getenv('container_name')
    dockerhub_login = os.getenv('dockerhub_login')

    build()

    if args.restart:
        restart()

    if args.push:
        push()

