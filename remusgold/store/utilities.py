from datetime import datetime
from os.path import splitext
from remusgold.settings import MEDIA_ROOT

def get_timestamp_path(instance, filename):
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])