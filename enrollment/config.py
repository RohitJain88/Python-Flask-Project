import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xd2\x1e@\x18\xeep\xe7\xd6c\x9fD&\xe5\xf6\xc2\x02'

    MONGODB_SETTINGS = { 'db' : 'UTA_Enrollment'}