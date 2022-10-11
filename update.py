from dotenv import load_dotenv
from logging import FileHandler, StreamHandler, INFO, basicConfig, error as log_error, info as log_info
from os import path as ospath, environ
from requests import get as rget
from subprocess import run as srun


basicConfig(format="%(asctime)s - %(levelname)s - [%(filename)s: %(lineno)d] - %(message)s",
                    handlers=[FileHandler('log.txt'), StreamHandler()],
                    level=INFO)


CONFIG_FILE_URL = environ.get('CONFIG_FILE_URL', '')
if CONFIG_FILE_URL:
    try:
        res = rget(CONFIG_FILE_URL)
        if res.status_code == 200:
            with open('config.env', 'wb+') as f:
                f.write(res.content)
        else:
            log_error(f"Failed to download config.env {res.status_code}")
    except Exception as e:
        log_error(f"CONFIG_FILE_URL: {e}")
load_dotenv('config.env', override=True)

if environ.get('UPDATE_EVERYTHING', 'True').lower() == 'true':
    srun(["pip3", "install", "-U", "--no-cache-dir", "-r", "requirements.txt"])

UPSTREAM_REPO = environ.get('UPSTREAM_REPO', None)
UPSTREAM_BRANCH = environ.get('UPSTREAM_BRANCH', None)

if ospath.exists('.git'):
    srun(["rm", "-rf", ".git"])

update = srun([f"git init -q \
                 && git config --global user.email omiduep@gmail.com \
                 && git config --global user.name OmiduSithul \
                 && git add . \
                 && git commit -sm update -q \
                 && git remote add origin {UPSTREAM_REPO} \
                 && git fetch origin -q \
                 && git reset --hard origin/{UPSTREAM_BRANCH} -q"], shell=True)

if update.returncode == 0:
    log_info('Successfully updated with latest commit from UPSTREAM_REPO')
else:
    log_error('Something went wrong while updating, check UPSTREAM_REPO if valid or not!')
