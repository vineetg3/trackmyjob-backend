import datetime
from datetime import timezone
import pytz

def get_current_IST_dt():
    IST = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(IST)
    return now
