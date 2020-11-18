import sys

import os

INTERP = os.path.expanduser("/home/mmzso01/zavivalovesky.ru/docs/venv/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

from flask_app import app
