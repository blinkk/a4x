import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'lib'))


_appid = os.getenv('APPLICATION_ID').replace('s~', '')
EMAIL_SENDER = 'noreply@{}.appspotmail.com'.format(_appid)
